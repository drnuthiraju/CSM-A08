import os

home_path = os.path.expanduser("~")

local_repo_path = os.path.join(home_path, "SWE-bench-repo")
virtual_env_path = os.path.join(home_path, "virtual_env")
os.makedirs(virtual_env_path, exist_ok=True)
exp_result_save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exp/SWE-bench")
exp_json_result_path = os.path.join(home_path, "exp/SWE-bench/assets/our_result")
db_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "sqlite_db/magis.db")
print(f"Database path: {db_path}")

API_TOKEN = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
cloudflare_account_id = "" # Edit this to your own account id
cloudflare_gateway = "" # Edit this to your own gateway

bm25_result_file_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "exp/SWE-bench/file_name_and_contents.retrieval_with_LLM.jsonl")
review=False