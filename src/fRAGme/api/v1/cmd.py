from fastapi import APIRouter, HTTPException
from fRAGme.util.v1.chroma_handler import *
from fRAGme.models.v1.cmd import *
from openai import OpenAI

router = APIRouter()


@router.post("/ask_question")
def cmd_ask_question(request: Question, identifier: str):
    try:
        prompt = build_question(request, identifier)
        client = OpenAI()

        chat_history = [
            {"role": element.role, "content": element.content}
            for element in request.chat_history
        ]
        chat_history.append({"role": RoleEnum.user, "content": prompt})

        completion = client.chat.completions.create(
            model="gpt-4o-mini", messages=chat_history
        )

        answer = completion.choices[0].message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"result": answer}
