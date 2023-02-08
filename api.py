from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

from conversation import load_conversation_chain, chat as chat_func

app = FastAPI()


class Conversation(BaseModel):
    input: str


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/chat/{conversation_id}")
def chat(conversation_id: str):
    history, _ = load_conversation_chain(conversation_id)
    conversation = [{"input": input, "output": output} for input, output in history]

    return { "history": conversation }

@app.post("/chat/{conversation_id}")
def chat(conversation_id: str, conversation: Conversation):
    print(conversation.input)
    history, _ = chat_func(conversation_id, conversation.input) 
    conversation = [{"input": input, "output": output} for input, output in history]

    return { "history": conversation }
