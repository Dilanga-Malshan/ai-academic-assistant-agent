"""Tasks 5-6: demonstrate query enhancement and grounded answer."""
from app.services.document_service import ingest_pdf
from app.chains.rag_chain import answer_question
ingest_pdf('project_guide.pdf')
print(answer_question('What are the expected deliverables?'))
print(answer_question('What is my personal final exam grade?'))
