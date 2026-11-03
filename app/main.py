"""Academic Assistant REST API. Local demonstration, NOT production auth."""
import logging
from threading import RLock
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import JSONResponse
from app.config import get_settings
from app.schemas import QueryRequest,ApprovalRequest,IngestResponse,AgentResponse
from app.services.document_service import ingest_pdf,is_indexed
from app.agents.academic_agent import ask_agent,review_agent

logger=logging.getLogger(__name__)
app=FastAPI(title='AI Academic Assistant Agent',version='1.0.0',description='Local RAG + human approval classroom demonstration')
_pending:dict[str,str]={}
_ownership_lock=RLock()

def map_error(exc:Exception):
    if isinstance(exc,FileNotFoundError): raise HTTPException(status_code=404,detail=str(exc)) from exc
    if isinstance(exc,ValueError): raise HTTPException(status_code=400,detail=str(exc)) from exc
    logger.exception('Unexpected model/service error')
    raise HTTPException(status_code=503,detail='AI service unavailable. Check Ollama, installed models, and application logs.') from exc

@app.get('/')
def home():return {'application':'AI Academic Assistant Agent','status':'ready','docs':'/docs'}

@app.get('/health')
def health():return {'status':'healthy','indexed_documents_available':is_indexed()}

@app.post('/ingest/{filename}',response_model=IngestResponse)
def ingest(filename:str):
    try:return ingest_pdf(filename)
    except Exception as exc:map_error(exc)

@app.post('/query',response_model=AgentResponse)
def query(payload:QueryRequest):
    if not is_indexed():raise HTTPException(status_code=400,detail='Index a document with /ingest/{filename} before querying.')
    try:result=ask_agent(payload.question,payload.user_id)
    except Exception as exc:map_error(exc)
    if result['status']=='approval_pending':
        with _ownership_lock:_pending[result['thread_id']]=payload.user_id
    return result

@app.post('/approve',response_model=AgentResponse)
def approve(payload:ApprovalRequest,x_demo_reviewer_token:str|None=Header(default=None)):
    settings=get_settings()
    if not settings.DEMO_MODE:raise HTTPException(status_code=403,detail='Demo review is disabled. Integrate real authentication first.')
    if settings.DEMO_REVIEWER_TOKEN=='replace-with-long-random-local-token':
        raise HTTPException(status_code=503,detail='Set a unique DEMO_REVIEWER_TOKEN in .env before testing approvals.')
    if x_demo_reviewer_token!=settings.DEMO_REVIEWER_TOKEN:
        raise HTTPException(status_code=403,detail='Reviewer token missing or invalid')
    with _ownership_lock:
        owner=_pending.get(payload.thread_id)
        if not owner:raise HTTPException(status_code=404,detail='No pending review for this thread (may have been lost on restart).')
        if owner!=payload.user_id:raise HTTPException(status_code=403,detail='Thread does not belong to this demo user.')
        del _pending[payload.thread_id]
    try:result=review_agent(payload.thread_id,payload.decision)
    except Exception as exc:
        with _ownership_lock:_pending[payload.thread_id]=payload.user_id
        map_error(exc)
    if result['status']=='approval_pending':
        with _ownership_lock:_pending[result['thread_id']]=payload.user_id
    return result
