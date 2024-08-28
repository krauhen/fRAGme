from typing import Dict, Any
from pydantic import BaseModel


class Text(BaseModel):
    text: str
    metadata: Dict[str, Any] = {"source": "text input"}


class TextUpdate(BaseModel):
    new_text: str
    new_metadata: Dict[str, Any]
