"""Task 1 and 5: prompting and semantic-query rewriting."""
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from app.config import get_settings

def model():
    s=get_settings()
    return ChatOllama(model=s.CHAT_MODEL,base_url=s.OLLAMA_BASE_URL,temperature=0)

def first_llm_chain(question: str) -> str:
    prompt=ChatPromptTemplate.from_template('You are a helpful Python academic tutor. Explain clearly: {question}')
    return (prompt | model()).invoke({'question':question}).content

def enhance_query(question: str) -> str:
    prompt=ChatPromptTemplate.from_messages([
       ('system','Rewrite this academic question to improve document semantic search. Preserve intent and any important terms. Expand useful abbreviations. Output ONLY one search query; never answer the question.'),
       ('human','{question}')])
    return str((prompt | model()).invoke({'question':question}).content).strip()
