from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Chat(BaseModel):
    message: str


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/chat/{conversation_id}")
def chat(conversation_id: str, chat: Chat):
    return {"conversation_id": conversation_id, "chat": chat.message}
