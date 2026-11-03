# Manual integration testing record — fill after actually running

Environment: Python version ______ | Ollama version ______ | Models ______ | Date ______

| Scenario | Actual response / screenshot name | Pass/Fail |
|---|---|---|
| API starts without errors | | |
| GET /health | | |
| POST /ingest/project_guide.pdf returns page/chunk counts | | |
| Missing PDF => 404 | | |
| Invalid extension => 400 | | |
| Semantic retrieval cites PDF source/page | | |
| Prompt rewrite preserves meaning | | |
| Answer supported by PDF | | |
| Unknown fact => insufficient-document answer | | |
| Agent calls retrieval tool | | |
| Agent requests protected file write | | |
| Approval returns completed and writes output/ | | |
| Rejection does not write output/ | | |
| Same thread ID resumes correctly | | |
| Invalid filename cannot escape output/ | | |

**Do not claim runtime tests passed without executing them.**
