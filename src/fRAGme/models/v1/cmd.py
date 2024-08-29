"""
This module contains models and enums used for the command API.
"""

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
    """Enum representing the role in a chat."""

    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


class ChatAction(BaseModel):
    """Model representing an action in a chat."""

    role: RoleEnum
    content: str


class Question(BaseModel):
    """Model representing a question with its context and parameters."""

    base_prompt: str = BASE_PROMPT
    chat_history: List[ChatAction]
    question: str
    k_similar_text_snippets: int = 10


class CmdAskQuestionRequest(BaseModel):
    """Model representing a request to ask a question."""

    info: Question
    identifier: str


class CmdAskQuestionResponse(BaseModel):
    """Model representing a response to the asked question."""

    result: ChatAction
