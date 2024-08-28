from enum import Enum
from typing import List
from pydantic import BaseModel

BASE_PROMPT = (
    "You are a RAG assistant and should answer questions according to the Info-Snippet you get.\n"
    "The prompt will have the following syntax:\n"
    "Question:\n{data.question}\n\n"
    "Info-Snippets:\n"
    "Text: {snippet.page_content}\n"
    "Metadata: {snippet.metadata}"
    "\n\n"
    "Text: {snippet.page_content}\n"
    "Metadata: {snippet.metadata}"
    "\n\n"
    "Text: {snippet.page_content}\n"
    "Metadata: {snippet.metadata}"
    "\n\n"
    "..."
)


class RoleEnum(str, Enum):
    user = "user"
    system = "system"
    assistant = "assistant"


class ChatAction(BaseModel):
    role: RoleEnum
    content: str


class Question(BaseModel):
    base_prompt: str = BASE_PROMPT
    chat_history: List[ChatAction]
    question: str
    k_similar_text_snippets: int = 2
