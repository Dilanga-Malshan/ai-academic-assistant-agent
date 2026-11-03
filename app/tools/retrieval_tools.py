"""Document retrieval tool for the agent."""
from langchain_core.tools import tool
from app.services.document_service import retrieve_documents,format_documents

@tool
def retrieve_context(enhanced_user_query: str) -> str:
    """Search indexed approved PDFs using a semantic query; returns quoted context with source filename/page metadata."""
    context,_=format_documents(retrieve_documents(enhanced_user_query))
    return context or 'No indexed academic PDF context is available.'
