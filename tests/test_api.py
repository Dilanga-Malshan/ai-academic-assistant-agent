"""API smoke tests run without needing Ollama."""
from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)

def test_home_and_health():
    assert client.get('/').status_code==200
    assert client.get('/health').json()['status']=='healthy'

def test_bad_ingest_filename():
    assert client.post('/ingest/not_a_pdf.txt').status_code==400

def test_missing_pdf():
    assert client.post('/ingest/missing.pdf').status_code==404

def test_blank_query():
    assert client.post('/query',json={'user_id':'student_001','question':' '}).status_code==422

def test_approval_requires_pending_thread():
    response=client.post('/approve',json={'user_id':'student_001','thread_id':'not-a-thread','decision':'approve'},headers={'x-demo-reviewer-token':'anything'})
    assert response.status_code in [404,403,503]
