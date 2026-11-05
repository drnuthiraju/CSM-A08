[![SVG Banners](https://svg-banners.vercel.app/api?type=origin&text1=MAGIS%20🧑‍💻&text2=💖%20GitHub%20Issue%20Resolusion&width=900&height=200)](https://github.com/Akshay090/svg-banners)


# 👉🏻 MAGIS 👈🏻


📃 <a href="https://arxiv.org/abs/2403.17927" target="_blank">arXiv Paper</a> ·  📓 <a href="https://proceedings.neurips.cc/paper_files/paper/2024/hash/5d1f02132ef51602adf07000ca5b6138-Abstract-Conference.html" target="_blank">NeurIPS 2024</a>  ·  ❞ <a href="#-citation"> Citation </a>


## ✨ Key Features

* 🪶 **Simple LLM-based Multi-Agent Framework for Software Evolution**

* 🔍 **Visualization of Multi-Agent Processing**


## 📦 Environment

> All commands below have been tested on a Linux-64 machine. The specified package versions are recommended, as they have been verified to work.

```bash
conda create -n magis python=3.11 -y
conda activate magis
conda install redis==5.0.3 -y  # If you need to cache repeated requests to the same LLM
pip install "openai>=1.0.0" pygments==2.17.2 pydeps==1.12.17 tiktoken==0.5.1 redis==5.0.1 flask==3.0.0 datasets==2.16.1
```

## 🚀 Run

To use MAGIS on a Git repository, please run the [magis.py](magis.py) script.  
You can view options and usage instructions by executing: `python magis.py --help`.


To reproduce our experiments on [SWE-bench](https://github.com/SWE-bench/SWE-bench/tree/b93ac87), please refer to [SWE-bench.md](exp/SWE-bench/README.md).



## 📖 Citation

If you find [MAGIS](https://github.com/co-evolve-lab/magis) useful for your research or applications, feel free to give us a star ⭐ or cite us using:

```bibtex
@inproceedings{magis,
  author       = {Wei Tao and
                  Yucheng Zhou and
                  Yanlin Wang and
                  Wenqiang Zhang and
                  Hongyu Zhang and
                  Yu Cheng},
  title        = {{MAGIS:} LLM-Based Multi-Agent Framework for GitHub Issue Resolution},
  booktitle    = {NeurIPS},
  year         = {2024}
}
```

## 🙏 Acknowledgements

- We thank the prior work, **[SWE-bench](https://arxiv.org/abs/2310.06770)** and [their responses for my question](https://github.com/SWE-bench/SWE-bench/issues/23).

- We gratefully acknowledge [OpenMoji](https://openmoji.org/) for providing the emojis used in our demonstrations.
# Multi-Agent Orchestrator for GitHub Issue Resolution

## 1. Project Overview

Modern software development projects continuously generate GitHub issues related to software bugs, feature requests, code refactoring, and performance improvements. Resolving these issues requires developers to understand the repository, identify relevant files and code, plan the required changes, implement the solution, validate it through testing, review the changes, and prepare a pull request.

This project aims to develop a **Multi-Agent Orchestrator for GitHub Issue Resolution**, an AI-assisted software engineering system that coordinates multiple specialized agents to automate major stages of repository-level GitHub issue resolution.

The project is based on the research presented in **MAGIS: LLM-Based Multi-Agent Framework for GitHub Issue Resolution**, published at NeurIPS 2024. MAGIS demonstrates that collaborative specialized agents can improve the ability of Large Language Models (LLMs) to resolve real-world GitHub issues. The proposed project will study this approach, implement its core concepts, identify practical limitations, and investigate improvements in orchestration, repository context retrieval, and LLM flexibility.

---

## 2. Research Problem

A single LLM can perform code generation and code understanding effectively at the function or file level. However, repository-level issue resolution involves several interconnected tasks:

- Understanding the GitHub issue
- Understanding the repository structure
- Locating relevant files and code
- Planning the required changes
- Modifying existing code
- Testing the modification
- Reviewing the generated solution
- Preparing the final change for human review

Processing an entire repository as context can be inefficient because large amounts of irrelevant information may be included. In addition, a software engineering system becomes less flexible when its orchestration workflow and LLM provider are tightly coupled.

Therefore, this project investigates how a **stateful multi-agent architecture with improved repository retrieval and configurable LLM support** can provide a more modular and practical approach to GitHub issue resolution.

---

## 3. Base Research Work

### Base Paper

**W. Tao, Y. Zhou, Y. Wang, W. Zhang, H. Zhang, and Y. Cheng, "MAGIS: LLM-Based Multi-Agent Framework for GitHub Issue Resolution," in Proceedings of the 38th Conference on Neural Information Processing Systems (NeurIPS), 2024.**

MAGIS proposes a multi-agent framework for repository-level GitHub issue resolution. The framework consists of four specialized agent roles:

### Manager Agent

Responsible for:

- Understanding and decomposing the GitHub issue
- Creating tasks
- Forming the development team
- Organizing planning discussions
- Coordinating the overall workflow

### Repository Custodian Agent

Responsible for:

- Locating files relevant to the GitHub issue
- Maintaining repository-related information
- Providing useful repository context to other agents

### Developer Agent

Responsible for:

- Performing the assigned development tasks
- Locating the required modification areas
- Generating and applying code changes

### Quality Assurance Agent

Responsible for:

- Reviewing generated code changes
- Identifying problems in the proposed solution
- Providing feedback to the Developer agent
- Supporting iterative correction

MAGIS evaluates its framework using the SWE-bench benchmark and demonstrates that structured collaboration among specialized agents can improve GitHub issue resolution compared with directly applying a single LLM.

---

## 4. Identified Research Gap

This project will not simply reproduce MAGIS. The MAGIS implementation will first be studied to understand its architecture and workflow, after which practical areas for extension will be investigated.

The main improvement areas are:

### 4.1 Modular Workflow Orchestration

The proposed system will use **LangGraph** to represent agents, states, transitions, conditional execution, and revision loops explicitly.

This will allow the workflow to be modified and extended without rewriting the complete orchestration logic.

### 4.2 Improved Repository Context Retrieval

The project will investigate **Retrieval-Augmented Generation (RAG)** for repository understanding.

Instead of providing large amounts of repository content to the LLM, the system will identify and retrieve the most relevant files, functions, and code chunks for a given issue.

### 4.3 Flexible LLM Integration

The proposed architecture will separate the LLM layer from the agent and orchestration layers.

A configurable interface will allow different LLM providers or locally hosted models to be used without redesigning the complete system.

### 4.4 Practical Deployment

The project will emphasize modularity, configurability, observability, and controlled deployment rather than attempting to build a fully autonomous replacement for human software developers.

The proposed improvements will be evaluated experimentally rather than assumed to improve performance in advance.

---

## 5. Proposed System

The proposed system will process a GitHub issue through multiple specialized agents coordinated by a central orchestrator.

### High-Level Workflow

```text
GitHub Issue
      |
      v
Issue Analysis
      |
      v
Repository Retrieval
      |
      v
Task Planning
      |
      v
Code Generation
      |
      v
Testing
      |
      +--------- Failure ---------+
      |                           |
      v                           |
Code Review <---------------------+
      |
      v
Final Patch
      |
      v
Pull Request Preparation
      |
      v
Human Review
```

The central orchestrator will maintain the state of the issue-resolution process and determine which agent should execute next.

---

## 6. Proposed Agent Structure

The final implementation will organize the system into the following logical agent roles.

### 1. Issue Analysis / Manager Agent

Responsibilities:

- Understand the issue description
- Identify the type and scope of the issue
- Break the issue into smaller tasks
- Identify task dependencies
- Produce a structured implementation plan

### 2. Repository Analysis / Retrieval Agent

Responsibilities:

- Inspect the repository structure
- Process relevant source files
- Build and maintain the retrieval index
- Retrieve relevant files and code chunks
- Provide focused context to downstream agents

### 3. Developer Agent

Responsibilities:

- Receive the implementation plan
- Analyze retrieved repository context
- Generate the required code modification
- Produce the proposed patch or modified file contents

### 4. Testing Agent

Responsibilities:

- Execute available project tests
- Identify test failures
- Determine whether failures are associated with the generated modification
- Return structured test results

### 5. Review / QA Agent

Responsibilities:

- Review the proposed modification
- Check whether the change addresses the issue
- Analyze test results and implementation quality
- Provide feedback for revision when required

### 6. Pull Request Agent

Responsibilities:

- Prepare the final patch information
- Generate a suitable pull-request title and description
- Prepare the solution for human review

The exact boundaries between agents may be refined during implementation based on experimental findings.

---

## 7. Repository Retrieval Strategy

Repository understanding is a major component of the proposed system.

The planned retrieval pipeline is:

```text
Repository
    |
    v
File Discovery
    |
    v
Code Parsing / Chunking
    |
    v
Embedding Generation
    |
    v
Vector Index
    |
    v
GitHub Issue
    |
    v
Query Embedding
    |
    v
Relevant Files / Code Chunks
    |
    v
Agent Context
```

The embedding model will be used for **retrieval**, not for final code generation.

Where practical, local embedding models will be used so that repository indexing and semantic retrieval do not depend on paid text-generation APIs.

The retrieval component will also be compared with a simpler keyword or BM25-based retrieval approach.

---

## 8. LLM Architecture

The LLM layer will be separated from the agent and orchestration logic.

Instead of connecting every agent directly to one specific provider, the system will use a common LLM interface.

```text
                LLM Interface
                      |
          +-----------+-----------+
          |           |           |
        Gemini       Groq      Local LLM
          |
    Other Providers
```

This design allows the underlying model to be changed without redesigning the entire agent workflow.

The development phase will prioritize free, low-cost, or locally available models where practical.

API credentials will be stored using environment variables and will never be committed to the repository.

---

# 9. Plan of Action

The project will be completed in the following stages.

## Phase 1 — Literature Study and Requirement Analysis

### Objective

Understand the research problem and related work before implementation.

### Tasks

- Study the MAGIS paper in detail
- Study the MAGIS GitHub implementation
- Study repository-level issue resolution
- Study the SWE-bench benchmark
- Study multi-agent systems and agent orchestration
- Study RAG and semantic code retrieval
- Study LangGraph and stateful workflows
- Identify the exact baseline and improvement areas

### Output

- Literature review
- Problem definition
- System requirements
- Initial architecture
- Finalized improvement objectives

---

## Phase 2 — MAGIS Baseline Analysis

### Objective

Understand the original approach before introducing modifications.

### Tasks

- Analyze the structure of the MAGIS repository
- Study its agent roles
- Study its planning workflow
- Study its repository retrieval mechanism
- Study its Developer and QA interaction
- Document the complete execution flow
- Run available components where practical

### Output

- MAGIS architecture documentation
- Baseline workflow
- Implementation observations
- Identified improvement opportunities

---

## Phase 3 — Basic Working Prototype

### Objective

Build a minimal end-to-end version of the proposed system.

### Tasks

- Connect the application with GitHub repositories
- Read repository structure
- Accept a GitHub issue
- Implement issue analysis
- Implement the initial agent workflow
- Generate a basic code modification
- Execute tests
- Produce a patch

### Output

A working prototype capable of processing a controlled GitHub issue from input to generated code changes.

---

## Phase 4 — LangGraph-Based Orchestration

### Objective

Develop the central stateful orchestration layer.

### Tasks

- Define the shared workflow state
- Represent agents as graph nodes
- Define transitions between agents
- Implement conditional routing
- Implement retry and failure handling
- Track intermediate results
- Add execution logging and tracing

### Output

A modular and stateful LangGraph-based multi-agent workflow.

---

## Phase 5 — RAG-Based Repository Retrieval

### Objective

Improve the way relevant repository context is identified and supplied to the agents.

### Tasks

- Parse repository files
- Filter irrelevant files and unsupported file types
- Split source code into meaningful chunks
- Generate embeddings
- Build the vector index
- Convert the GitHub issue into a retrieval query
- Retrieve relevant files and code chunks
- Pass only relevant context to downstream agents
- Compare retrieval performance with a keyword/BM25 baseline

### Output

An integrated repository retrieval module using semantic search and RAG.

---

## Phase 6 — Multi-LLM Support

### Objective

Remove dependence on a single LLM provider.

### Tasks

- Define a common LLM interface
- Implement the primary LLM provider
- Implement at least one alternative provider
- Support model selection through configuration
- Handle API failures and rate limits
- Keep credentials outside the source code

### Output

A provider-independent LLM layer.

---

## Phase 7 — Testing and Validation

### Objective

Validate generated code before finalizing the solution.

### Tasks

- Execute the repository's available test suite
- Record test results
- Detect failures introduced by generated changes
- Return failure information to the appropriate agent
- Perform bounded revision cycles
- Re-run tests after revisions
- Prepare the final patch after validation

### Output

An automated testing, review, and correction loop.

---

## Phase 8 — Evaluation

### Objective

Measure the effectiveness of the proposed system and its individual improvements.

The evaluation will focus on measurable system behavior.

### Retrieval Metrics

- Precision of retrieved files or code chunks
- Recall of relevant repository files
- Number of retrieved files required to provide sufficient context

### Code Metrics

- Patch applicability
- Syntax or compilation validity
- Test pass rate
- Number of revision cycles

### Workflow Metrics

- Successful completion rate
- Number of failed agent executions
- End-to-end execution time
- Percentage of workflow stages automated

### Efficiency Metrics

- Number of LLM requests
- Approximate token usage
- Context size
- Retrieval latency

Where sufficient resources are available, evaluation will be performed on a controlled subset of SWE-bench or suitable real-world GitHub issues.

---

# 10. Baseline and Comparative Evaluation

The project will use incremental evaluation so that the effect of each major improvement can be studied separately.

```text
MAGIS-Inspired Baseline
          |
          v
+ LangGraph Orchestration
          |
          v
+ Improved Repository Retrieval / RAG
          |
          v
+ Multi-LLM Support
          |
          v
Final Proposed System
```

This approach will help determine which components contribute to the final system rather than treating the complete system as a single unexplained modification.

---

# 11. Scope

## In Scope

- GitHub issue analysis
- Repository understanding
- Relevant code retrieval
- Multi-agent task planning
- Code generation
- Automated testing
- Code review
- Iterative correction
- Pull request preparation
- Configurable LLM providers
- Evaluation on selected GitHub issues

## Out of Scope

- Training a new Large Language Model
- Replacing human software developers
- Guaranteeing resolution of every GitHub issue
- Autonomous merging into a production branch
- Supporting every programming language from the initial version
- Large-scale commercial deployment

The initial implementation will focus on a controlled set of repositories and programming languages so that reliable development and evaluation can be achieved within the project timeline.

---

# 12. Cost-Conscious Development Strategy

The system is designed to minimize unnecessary dependence on paid APIs.

Repository operations such as file scanning, parsing, chunking, indexing, and retrieval will be performed locally wherever practical.

LLM calls will primarily be used for tasks requiring reasoning, planning, code generation, or review.

The development strategy will prioritize:

- Free-tier or low-cost LLM access
- Local embedding models
- Local vector storage
- Response caching where appropriate
- Small controlled experiments during development
- Provider-independent architecture

This design allows development to continue even if a particular LLM provider becomes temporarily unavailable.

---

# 13. Technology Stack

| Component | Planned Technology |
|---|---|
| Programming Language | Python |
| Agent Orchestration | LangGraph |
| LLM Integration | Configurable Provider Interface |
| Primary Development Model | Gemini |
| Alternative Model | Groq / Other Compatible Provider |
| Repository Operations | Git / GitPython |
| GitHub Integration | GitHub API / PyGithub |
| Retrieval | Retrieval-Augmented Generation (RAG) |
| Embeddings | Local Embedding Model |
| Vector Store | ChromaDB / FAISS |
| Backend API | FastAPI |
| Testing | Repository-Native Test Framework |
| Containerization | Docker |
| Version Control | GitHub |

The exact technology choices may be refined during implementation based on compatibility, performance, and experimental results.

---

# 14. Expected Final System

The expected workflow of the final prototype is:

```text
User selects GitHub Repository
            |
            v
User provides GitHub Issue
            |
            v
Issue Analysis
            |
            v
Repository Retrieval
            |
            v
Task Planning
            |
            v
Developer Agent
            |
            v
Testing
       /              Pass           Fail
      |              |
      v              v
   Review        Feedback
      |              |
      +--------------+
             |
             v
   Final Validated Patch
             |
             v
   Pull Request Preparation
             |
             v
       Human Review
```

---

# 15. Expected Contribution

The project aims to develop a modular and practical multi-agent framework for repository-level GitHub issue resolution by combining:

1. Stateful graph-based agent orchestration
2. Efficient repository context retrieval using RAG
3. Configurable support for multiple LLM providers
4. Automated testing and iterative correction
5. Measurable evaluation of retrieval, code generation, and workflow performance

The final contribution will be determined by the experimental results obtained during implementation rather than assuming in advance that every proposed modification will improve performance.

---

# 16. Team Development Workflow

All development will be managed through the project GitHub repository.

### Suggested Branch Structure

```text
main
 |
 +-- development
      |
      +-- feature/langgraph
      +-- feature/retrieval
      +-- feature/agents
      +-- feature/testing
      +-- feature/github
      +-- feature/llm
```

Each team member will work on a separate feature branch and submit changes through pull requests.

Changes will be reviewed and tested before being merged into the development branch and eventually into the main branch.

---

# 17. Project Deliverables

## Review 0

- Base research paper
- At least three relevant references
- Project abstract
- Project GitHub repository
- README.md containing the project plan of action

## Development Stage

- MAGIS analysis
- System architecture
- LangGraph workflow
- Agent implementations
- Repository retrieval module
- LLM provider interface
- Testing and validation pipeline

## Final Stage

- Working prototype
- Experimental results
- Comparative evaluation
- Technical documentation
- Final project report
- Project demonstration

---

# 18. Success Criteria

The project will be considered successful when the implemented system can:

- Accept a GitHub issue and repository
- Identify relevant repository context
- Generate a structured solution plan
- Produce a valid code modification
- Execute available repository tests
- Use testing or review feedback for bounded revision
- Prepare a final patch or pull request
- Demonstrate measurable retrieval and issue-resolution performance on selected evaluation cases
- Switch the underlying LLM provider without redesigning the complete orchestration architecture

---

# 19. Future Extensions

Possible future extensions include:

- Advanced semantic and AST-based code retrieval
- Repository-specific long-term memory
- Security analysis agents
- Human-in-the-loop approval interfaces
- Support for additional programming languages
- Larger-scale SWE-bench evaluation
- Cost-aware model routing
- Production-grade GitHub App deployment

---

## 20. References

1. W. Tao, Y. Zhou, Y. Wang, W. Zhang, H. Zhang, and Y. Cheng, "MAGIS: LLM-Based Multi-Agent Framework for GitHub Issue Resolution," in Proceedings of the 38th Conference on Neural Information Processing Systems (NeurIPS), 2024.  
   Paper: https://arxiv.org/abs/2403.17927  
   GitHub: https://github.com/co-evolve-lab/magis

2. J. Yang, C. E. Jimenez, A. Wettig, K. Lieret, S. Yao, K. Narasimhan, and O. Press, "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering," in Advances in Neural Information Processing Systems (NeurIPS), 2024.

3. C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. Narasimhan, "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" in Proceedings of the 12th International Conference on Learning Representations (ICLR), 2024.

4. K. Koech, M. Adam, B. B. Jean Jacques, and J. Barros, "Phoenix: Safe GitHub Issue Resolution via Multi-Agent LLMs," arXiv preprint arXiv:2606.20243, 2026.
