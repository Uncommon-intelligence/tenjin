#!/usr/bin/env python
import os
from typing import Optional, Union
from fastapi import BackgroundTasks, FastAPI, Request
from pydantic import BaseModel
from slack_sdk import WebClient
import tenjin.config
from tenjin.conversation import load_conversation_chain, chat as chat_func
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

app = FastAPI()
slack_client = WebClient(token=tenjin.config.slack_token)


class Conversation(BaseModel):
    challenge: Optional[str] = None
    input: Optional[str] = None

class SlackChallenge(BaseModel):
    challenge: str
    token: str
    type: str

def _handle_app_mention(event: dict) -> None:
    thread_ts = event.get("thread_ts") or event.get("ts")
    channel = event.get("channel")
    conversation_id = f"{channel}-{thread_ts}"
    history, _ = chat_func(conversation_id, event['text']) 
    conversation = [{"input": input, "output": output} for input, output in history]
    text = conversation[-1]["output"]

    slack_client.chat_postMessage(channel=channel, thread_ts=thread_ts, text=text)

def respond_to_slack_message(event):
    if not event.get("bot_id"):
        _handle_app_mention(event)

@app.post("/conversation")
async def slack_event(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()
    event = body.get("event")

    if event:
        background_tasks.add_task(respond_to_slack_message, event)

    return { "challenge": body.get("challenge", None) }

@app.get("/chat/{conversation_id}")
def chat(conversation_id: str):
    history, _ = load_conversation_chain(conversation_id)
    conversation = [{"input": input, "output": output} for input, output in history]

    return { "history": conversation }

@app.post("/chat/{conversation_id}")
def chat(conversation_id: str, conversation: Conversation) -> dict:
    history, _ = chat_func(conversation_id, conversation.input) 
    conversation = [{"input": input, "output": output} for input, output in history]

    return { "history": conversation }

def serve(host:str = "0.0.0.0", port:int = 8000) -> None:
    import uvicorn
    uvicorn.run(app, host=host, port=port)