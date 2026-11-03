"""Query enhancement tool exposed to the academic agent."""
from langchain_core.tools import tool
from app.chains.query_chain import enhance_query

@tool
def enhance_user_query(user_query: str) -> str:
    """Rewrite the student's academic question into a focused semantic search query; returns query text, not an answer."""
    return enhance_query(user_query)
