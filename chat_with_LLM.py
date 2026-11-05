import json
import time
import os
import math
import threading
import openai
import hashlib
import tiktoken
import requests

try:
    import redis
except ImportError:
    redis = None

import config
from log import log
logger = log(__name__).get_log_obj()

API_TOKEN = config.API_TOKEN

_redis_warning_logged = False
_gemini_request_lock = threading.Lock()
_last_gemini_request_at = None
                    
class ResponseException(Exception):
    def __init__(self, info_dict):
        super().__init__(str(info_dict))
        self._info_dict = info_dict
        if 'message' in info_dict.keys():
            self._info_dict['_message'] = info_dict['message']

    def __getattr__(self, item):
        try:
            return self._info_dict[item]
        except KeyError:
            raise AttributeError(f"'ResponseException' object has no attribute '{item}'")


class LLMRequestError(RuntimeError):
    pass


def _error_details(error):
    body = getattr(error, "body", None)
    if isinstance(error, ResponseException):
        body = error._info_dict
    details = body.get("error", body) if isinstance(body, dict) else {}
    message = str(error)
    if isinstance(details, dict):
        message = str(details.get("message", message))
    code = getattr(error, "code", None)
    if isinstance(details, dict):
        code = code or details.get("code") or details.get("status")
    return getattr(error, "status_code", None), str(code or "").lower(), message


def _cache_client():
    global _redis_warning_logged
    if redis is None:
        if not _redis_warning_logged:
            logger.warning("Redis package is unavailable; continuing without response caching.")
            _redis_warning_logged = True
        return None
    return redis.StrictRedis(host='localhost', port=6379, db=0)


def _gemini_min_request_interval_seconds():
    value = os.environ.get("GEMINI_MIN_REQUEST_INTERVAL_SECONDS", "13")
    try:
        interval = float(value)
        if not math.isfinite(interval):
            raise ValueError
        return max(13.0, interval)
    except ValueError:
        logger.warning("Invalid GEMINI_MIN_REQUEST_INTERVAL_SECONDS; using 13 seconds.")
        return 13.0


def _create_gemini_completion(client, model_name, messages):
    global _last_gemini_request_at
    with _gemini_request_lock:
        now = time.monotonic()
        if _last_gemini_request_at is not None:
            wait_seconds = _gemini_min_request_interval_seconds() - (now - _last_gemini_request_at)
            if wait_seconds > 0:
                time.sleep(wait_seconds)
        _last_gemini_request_at = time.monotonic()
        return client.chat.completions.create(model=model_name, messages=messages)


def request_api(model_name, user_prompt, system_prompt, channel = "openai",
                account_id = config.cloudflare_account_id, gateway=config.cloudflare_gateway):
    if channel == "openai":
        if not API_TOKEN:
            raise LLMRequestError("GEMINI_API_KEY is not set in the environment.")
        client = openai.OpenAI(
            api_key=API_TOKEN,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
        response = _create_gemini_completion(
            client,
            model_name,
            [{"role": "system", "content": system_prompt},
             {"role": "user", "content": user_prompt}],
        )
        return response.model_dump()
    elif channel  == "cloudflare":
        if "gpt" in model_name:
            API_BASE_URL = f"https://gateway.ai.cloudflare.com/v1/{account_id}/{gateway}/openai/chat/completions"
            headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
            data = {"model": model_name,
                    "messages": [{"role": "system", "content": system_prompt},
                                 {"role": "user", "content": user_prompt}]}
        response = requests.post(API_BASE_URL, headers=headers, json=data, timeout=60*10)
        logger.info(response.text)
        return json.loads(response.text)
    else:
        raise ValueError(f"Invalid channel: {channel}")


def atomic_chat(system_prompt, user_prompt, max_times=5, model_name=None, use_cache=False):
    max_attempts = max(1, min(int(max_times), 5))
    cache = None
    if use_cache:
        cache = _cache_client()
        if cache is not None:
            all_prompt = model_name + system_prompt + user_prompt
            cache_key = hashlib.sha256(all_prompt.encode()).hexdigest()
            try:
                cached_response = cache.get(cache_key)
                if cached_response:
                    return json.loads(cached_response)
            except Exception as e:
                logger.warning(f"Redis cache unavailable; continuing without caching: {e}")
                cache = None

    for try_i in range(max_attempts):
        try:
            response = request_api(model_name, user_prompt, system_prompt)
            if "error" in response.keys():
                raise ResponseException(response["error"])
            if "detail" in response.keys() and "This model's maximum context length is 32768 tokens. However, you requested " in response["detail"]:
                raise ResponseException({"code": "context_length_exceeded", "_message": response["detail"]})
            if cache is not None:
                try:
                    cache.setex(cache_key, 60*60*24*365, json.dumps(response))
                except Exception as e:
                    logger.warning(f"Redis cache unavailable; continuing without caching: {e}")
            return response
        except Exception as e:
            status_code, code, message = _error_details(e)
            normalized_message = message.lower()
            quota_exhausted = "quota" in normalized_message and any(
                token in normalized_message for token in ("exceed", "limit", "exhaust")
            )
            if quota_exhausted:
                raise LLMRequestError(f"Gemini quota exhausted: {message}") from e

            rate_limited = str(status_code) == "429" or code in ("429", "resource_exhausted", "rate_limit_exceeded") or "resource_exhausted" in normalized_message or "http 429" in normalized_message
            if rate_limited and try_i + 1 < max_attempts:
                delay = min(2 ** try_i, 8)
                logger.warning(f"Gemini rate limit/resource exhaustion; retry {try_i + 1}/{max_attempts - 1} in {delay}s.")
                time.sleep(delay)
                continue
            if rate_limited:
                raise LLMRequestError(f"Gemini rate limit or quota exhaustion persisted after {max_attempts} attempts: {message}") from e
            raise LLMRequestError(f"LLM request failed: {message}") from e

    raise LLMRequestError(f"LLM request failed after {max_attempts} attempts.")


def chat(system_prompt, user_prompt, model_name, output_format = None, use_cache=False, remove_quote=False,
         db_manager=None, request_index=None):
    response = atomic_chat(system_prompt, user_prompt, model_name=model_name, use_cache=use_cache)

    if db_manager is not None and request_index is not None:
        db_manager.add_response(request_index, response)
    else:
        logger.debug(response)
    try:
        print(response)
        if "choices" not in response.keys() and "messages" in response.keys():
            response_txt = response['messages'][-1]['content']
        elif "choices" in response.keys() and len(response['choices']) > 0:
            response_txt = response['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"Error: {e}\nresponse:{response}")
        exit(1)
    if output_format is not None:
        check_system_prompt = "You are an Information Extraction Expert. You check if the output strictly follows the format."
        check_user_prompt = f"Please determine whether the following Content (between '```' and '```') meets the Format. If so, output just 'True'. Otherwise, extract the content part that strictly follows the Format from the Content as output.\nContent:```{response_txt}```\nFormat:{output_format}"
        check_response = atomic_chat(check_system_prompt, check_user_prompt, model_name=model_name, use_cache=use_cache)
        if not check_response['choices'][0]['message']['content'] == "True":
            response_txt = check_response['choices'][0]['message']['content']

    if remove_quote:
        if (response_txt[0] == "\'" and response_txt[-1] == "\'") or \
            (response_txt[0] == "\"" and response_txt[-1] == "\""):
            response_txt = response_txt[1:-1]
        if response_txt == "":
            response_txt = "<NONE>"
    return response_txt
