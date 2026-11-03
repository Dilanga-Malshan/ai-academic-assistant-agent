"""Tasks 2-4: ingest a PDF, inspect metadata, and search."""
from app.services.document_service import ingest_pdf,retrieve_documents
print(ingest_pdf('project_guide.pdf'))
for match in retrieve_documents('What should students submit?'):
    print(match.metadata,match.page_content[:300])
