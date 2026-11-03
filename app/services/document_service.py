"""PDF ingestion, vector indexing, and context retrieval."""
import re
from pathlib import Path
from threading import RLock
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import DOCUMENTS_DIR, get_settings

_store: InMemoryVectorStore | None = None
_indexed: set[str] = set()
_lock = RLock()

def safe_pdf_path(filename: str) -> Path:
    """Return an existing PDF inside documents; reject traversal and symlinks."""
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*\.pdf',filename,re.IGNORECASE):
        raise ValueError('Use a plain PDF filename, e.g. assignment_guide.pdf')
    if filename in {'.pdf','..pdf'}: raise ValueError('Invalid filename')
    path = DOCUMENTS_DIR / filename
    if path.is_symlink() or not path.is_file() or path.resolve().parent != DOCUMENTS_DIR.resolve():
        raise FileNotFoundError('PDF was not found inside documents/')
    return path

def _get_store() -> InMemoryVectorStore:
    global _store
    if _store is None:
        s = get_settings()
        _store = InMemoryVectorStore(embedding=OllamaEmbeddings(model=s.EMBEDDING_MODEL,base_url=s.OLLAMA_BASE_URL))
    return _store

def ingest_pdf(filename: str) -> dict:
    """Load PDF pages, preserve source/page metadata, and index chunks."""
    path = safe_pdf_path(filename)
    pages = PyPDFLoader(str(path)).load()
    if not pages or not any(page.page_content.strip() for page in pages):
        raise ValueError('PDF has no extractable text; scanned PDFs may need OCR')
    s = get_settings()
    splitter = RecursiveCharacterTextSplitter(chunk_size=s.CHUNK_SIZE,chunk_overlap=s.CHUNK_OVERLAP)
    chunks = splitter.split_documents(pages)
    for part in chunks:
        part.metadata['source'] = path.name
        part.metadata['page_number'] = int(part.metadata.get('page',0)) + 1
    with _lock:
        if filename in _indexed:
            return {'filename':filename,'pages':len(pages),'chunks':len(chunks),'message':'PDF already indexed for this server session.'}
        _get_store().add_documents(chunks)
        _indexed.add(filename)
    return {'filename':filename,'pages':len(pages),'chunks':len(chunks),'message':'PDF indexed successfully.'}

def retrieve_documents(query: str, k: int | None = None):
    if not query.strip(): raise ValueError('Search query must not be blank')
    with _lock:
        if not _indexed: return []
        return _get_store().similarity_search(query,k=k or get_settings().RETRIEVAL_TOP_K)

def format_documents(documents) -> tuple[str,list[dict]]:
    parts=[]; sources=[]
    for i,d in enumerate(documents,1):
        source=d.metadata.get('source','unknown.pdf')
        page=d.metadata.get('page_number',int(d.metadata.get('page',0))+1)
        parts.append(f'[Document {i}: {source}, page {page}]\n{d.page_content}')
        marker={'filename':source,'page':page}
        if marker not in sources:sources.append(marker)
    return '\n\n'.join(parts),sources

def is_indexed() -> bool: return bool(_indexed)
