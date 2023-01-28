from typing import List
from langchain import PromptTemplate
from langchain.chains.conversation.memory import ConversationalBufferWindowMemory


def book_prompt(buffer=List[str]):
    """
    Returns a contextualized prompt for the chatbot

    Returns:
        prompt: contextualized prompt
        memory: memory to use for the chatbot
    """
    template = """
    You are a chatbot having a converesation with a human about the contents of a book or paper.
    You should respond to the human's question with a relevant sentence from the document as if you were the author of the document.
    If there is more than one author, reply as if you were the author of the most relevant sentence.
    Answers should be written in markdown format.

    {context}

    {chat_history}
    Human: {question}
    Chatbot:
    """

    prompt = PromptTemplate(
        input_variables=["chat_history", "question", "context"],
        template=template,
    )

    memory = ConversationalBufferWindowMemory(
        memory_key="chat_history",
        input_key="question",
        buffer=buffer,
    )

    return prompt, memory
