"""Offline safety and API validation checks (no Ollama required)."""
import pytest
from pydantic import ValidationError
from app.schemas import QueryRequest,ApprovalRequest
from app.services.document_service import safe_pdf_path
from app.tools.file_tools import safe_output_path

@pytest.mark.parametrize('name',['../secret.pdf','C:\\secret.pdf','notes.txt','/etc/passwd','..pdf'])
def test_bad_pdf_names(name):
    with pytest.raises((ValueError,FileNotFoundError)):safe_pdf_path(name)

@pytest.mark.parametrize('name',['../escape.txt','sub/f.txt','hello.pdf','.txt','a..txt','foo.txt/../../x'])
def test_bad_output_names(name):
    with pytest.raises(ValueError):safe_output_path(name)

def test_valid_output_filename():assert safe_output_path('llm_requirements.txt').name=='llm_requirements.txt'

def test_blank_question():
    with pytest.raises(ValidationError):QueryRequest(user_id='student_001',question='   ')

def test_bad_decision():
    with pytest.raises(ValidationError):ApprovalRequest(user_id='student_001',thread_id='t',decision='delete')
