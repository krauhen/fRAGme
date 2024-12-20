import fRAGme
from fRAGme.models.cmd import Question, ChatAction


def test_basic(api_key):
    print()
    question = "What is the capital of France?"
    print("Q: ", question)
    question = Question(question=question)
    answer = fRAGme.ask(question, api_key)
    print("A:", answer.content)
    print()

    ########################################
    ########################################
    ########################################

    chat_history = [ChatAction(content=answer.content, role=answer.role)]

    question = "And what is the highest building there?"
    print("Q: ", question)
    question = Question(question=question, chat_history=chat_history)
    answer = fRAGme.ask(question, api_key)
    print("A:", answer.content)
    print()
