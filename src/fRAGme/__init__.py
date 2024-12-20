"""This is a dockerized RAG FastAPI service with vector store handling."""

__version__ = "0.1.13"

from openai import OpenAI
from fRAGme.models.cmd import RoleEnum, Question, ChatAction
from fRAGme.util.chroma_handler import build_question


def ask(question: Question, api_key: str, identifier: str = "base"):

    prompt = build_question(question, identifier, api_key)
    client = OpenAI(api_key=api_key)

    chat_history = [
        {"role": element.role, "content": element.content}
        for element in question.chat_history
    ]
    chat_history.append({"role": RoleEnum.USER, "content": prompt})

    completion = client.chat.completions.create(
        model="gpt-4o-mini", messages=chat_history
    )

    answer = completion.choices[0].message
    return answer
