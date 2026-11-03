"""Restricted output text writer. HITL middleware protects calls from the agent."""
import re
from pathlib import Path
from langchain_core.tools import tool
from app.config import OUTPUT_DIR

def safe_output_path(file_name: str) -> Path:
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}\.txt',file_name,re.IGNORECASE):
        raise ValueError('Use a simple .txt filename without paths or dots in the basename')
    path=OUTPUT_DIR/file_name
    if path.is_symlink() or path.resolve().parent != OUTPUT_DIR.resolve():
        raise ValueError('Invalid output path')
    return path

@tool
def write_results_to_file(content: str, file_name: str) -> str:
    """Append user-requested academic summary text to a safe .txt file in output/; MUST require reviewer approval before agent execution."""
    if not content.strip(): raise ValueError('Refusing to save empty content')
    path=safe_output_path(file_name)
    with path.open('a',encoding='utf-8') as handle:
        handle.write(content.rstrip()+'\n\n')
    return f'Content saved to output/{path.name}'
