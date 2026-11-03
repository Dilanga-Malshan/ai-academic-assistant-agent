# AI Academic Assistant Agent

A document-aware academic assistant implementing the **12-page AI Academic Assistant — Student Project Guide** with LangChain, local Ollama, RAG, LangGraph human approval, and FastAPI.

> **Classroom prototype only.** Not a production student information system. Model responses are grounded in approved academic documents and should not invent deadlines, grades or policies.

## Features

- Load approved PDFs with `PyPDFLoader`, retain filenames and page metadata.
- Split text with overlapping chunks, create `OllamaEmbeddings`, and store vectors in `InMemoryVectorStore`.
- Rewrite student questions for semantic retrieval using a LangChain prompt chain.
- Produce grounded RAG answers with source references and a missing-evidence fallback.
- Use an AI agent with query-enhancement, retrieval and output-file tools.
- Pause protected file-write operations for reviewer approval via LangGraph checkpointing and `HumanInTheLoopMiddleware`.
- Expose REST endpoints with FastAPI and Pydantic validation.
- Include tests for API input validation and filesystem safety.

## Requirements

Python 3.11–3.13 recommended, Ollama installed and running locally, and Python packages from `requirements.txt`. The project uses local chat model `llama3.2` and embedding model `nomic-embed-text`.

## Windows / PyCharm setup

Run from this repository root:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
ollama pull llama3.2
ollama pull nomic-embed-text
python -m uvicorn app.main:app --reload
```

Before starting, change the placeholder `DEMO_REVIEWER_TOKEN` in your local `.env` to a long private random value. Do not commit `.env`. Use `http://127.0.0.1:8000/docs` to open Swagger UI.

## Academic PDF setup

Put a **lecturer-approved text-based PDF** inside `documents/`, such as `assignment_guide.pdf`. This repository currently includes the document folder instructions, **not** the guide PDF itself. The separately delivered full project ZIP includes a sample `project_guide.pdf` that can be placed here. Scanned PDFs require separate OCR support.

Index a PDF before querying; the in-memory index disappears after a restart.

## API

| Route | Purpose |
|---|---|
| `GET /` | Welcome/status |
| `GET /health` | Service health |
| `POST /ingest/{filename}` | Index PDF in `documents/` |
| `POST /query` | Question / agent response |
| `POST /approve` | Resume protected action with approve/reject |

Example request for `POST /query`:

```json
{"user_id":"student_001","question":"What must I submit for my assignment?"}
```

Example save request:

```json
{"user_id":"student_001","question":"Summarize the assignment requirements and save them as requirements.txt"}
```

The agent may return `approval_pending` and a `thread_id`. Inspect the pending actions, then call `POST /approve` with:

```json
{"user_id":"student_001","thread_id":"THREAD_ID_FROM_QUERY","decision":"approve"}
```

Supply the `x-demo-reviewer-token` header configured in `.env`. A rejection uses `"decision":"reject"`. Use a fresh save request to test both outcomes. Use a `.txt` basename allowed by `safe_output_path`; the approval tool only appends to files in `output/`.

**Security warning:** `user_id` in an HTTP body is not authenticated identity. The reviewer token is only a controlled local demo. Do not expose the prototype publicly without real authentication, authorization, action ownership checks, and persistent storage.

## Tests

```powershell
python -m pytest -q
```

The automated tests do not replace full Ollama and LangGraph integration testing. Use `TEST_EVIDENCE_TEMPLATE.md` to record actual ingestion, retrieval, grounding, file approval, and rejection. Do **not** claim tests passed without running them.

## Project structure

```text
app/
  main.py
  config.py
  schemas.py
  chains/query_chain.py
  chains/rag_chain.py
  services/document_service.py
  tools/query_tools.py
  tools/retrieval_tools.py
  tools/file_tools.py
  agents/academic_agent.py
documents/
examples/
tests/
output/  (created automatically)
.env.example
.gitignore
requirements.txt
TEST_EVIDENCE_TEMPLATE.md
```

## Notes

The PDF-specific project guide requests that each milestone is understood, implemented, tested and demonstrated. InMemoryVectorStore and InMemorySaver lose data after process restart. Real deployments require persistence and stronger security. Current LangChain/LangGraph APIs can evolve, so record compatible package versions after verifying the local environment.

## License

For educational use. No specific license has been granted for external third-party documents.
