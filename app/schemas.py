"""Pydantic API contracts."""
from typing import Literal
from pydantic import BaseModel, Field, field_validator

class QueryRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=80, pattern=r'^[a-zA-Z0-9_-]+$')
    question: str = Field(min_length=1, max_length=4000)
    @field_validator('question')
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip(): raise ValueError('Question must not be blank')
        return value.strip()

class ApprovalRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=80, pattern=r'^[a-zA-Z0-9_-]+$')
    thread_id: str = Field(min_length=1, max_length=160)
    decision: Literal['approve','reject']

class IngestResponse(BaseModel):
    filename: str
    pages: int
    chunks: int
    message: str

class AgentResponse(BaseModel):
    status: Literal['completed','approval_pending']
    thread_id: str
    answer: str | None = None
    pending_actions: list[dict] = Field(default_factory=list)
