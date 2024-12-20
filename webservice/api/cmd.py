"""
This module provides an API endpoint to ask questions against a vector store
using OpenAI's language model.
"""

from typing import Annotated

import fRAGme
from fastapi import APIRouter, HTTPException, Depends

from fRAGme.models.v1.auth import User
from fRAGme.util.v1.auth import get_current_active_user
from fRAGme.models.v1.cmd import (
    CmdAskQuestionRequest,
    CmdAskQuestionResponse,
    ChatAction,
)

router = APIRouter()


@router.post("/ask_question", response_model=CmdAskQuestionResponse)
def cmd_ask_question(
    request: CmdAskQuestionRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Endpoint to ask a question against a vector store.

    Args:
        request: A request object containing parameters.

    Returns:
        A ChatAction element with the role and the content of the answer.

    Raises:
        HTTPException: Generic internal server error.
    """
    try:
        answer = fRAGme.ask(request.info, request.identifier)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return CmdAskQuestionResponse(
        result=ChatAction(role=answer.role, content=answer.content)
    )
