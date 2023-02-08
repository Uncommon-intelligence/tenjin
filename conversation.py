import os
import uuid
import toml
import boto3
import json
import gradio as gr
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.agents import Tool, initialize_agent
from langchain.chains.conversation.memory import ConversationalBufferWindowMemory
from langchain.utilities import GoogleSearchAPIWrapper

BUCKET_NAME = "conversations"

with open("config.toml") as f:
    config = toml.load(f)

os.environ["OPENAI_API_KEY"] = config["openai"]["api_key"]
os.environ["GOOGLE_API_KEY"] = config["google"]["api_key"]
os.environ["GOOGLE_CSE_ID"] = config["google"]["cse_id"]

search = GoogleSearchAPIWrapper()

s3 = boto3.client("s3", endpoint_url="http://localhost:4566")


def upload_json_to_s3(file_name: str, payload: dict):
    s3.create_bucket(Bucket=BUCKET_NAME)
    s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=json.dumps(payload))


def fetch_conversation_data(file_name: str):
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=file_name)
        json_data = response["Body"].read().decode("utf-8")

        conversation = json.loads(json_data)
    except:
        conversation = {}

    history = conversation.get("history", [])
    buffer = conversation.get("buffer", [])

    return history, buffer

tools = [
    Tool(
        name="Google Search",
        func=search.run,
        description="Search the web with Google",
    )
]

llm = OpenAI(
    temperature=0,
    max_tokens=1000,
    model_name="text-davinci-003",
)


def load_conversation_chain(conversation_id: str):
    history, buffer = fetch_conversation_data(conversation_id)

    memory = ConversationalBufferWindowMemory(
        k=10, memory_key="chat_history", buffer=buffer
    )

    chain = initialize_agent(
        tools=tools,
        llm=llm,
        agent="conversational-react-description",
        verbose=True,
        memory=memory,
    )

    return history, chain


def chat(conversation_id, user_input):
    history, chain = load_conversation_chain(conversation_id)
    response = chain(user_input)

    history.append((response["input"], response["output"]))

    upload_json_to_s3(
        file_name=conversation_id,
        payload={
            "buffer": chain.memory.buffer,
            "history": history,
        },
    )

    return history, ""

def reset_chat():
    return [], uuid.uuid4()


with gr.Blocks() as demo:
    with gr.Tab("Chat"):
        conversation_id = gr.Textbox(lines=1, value=uuid.uuid4(), show_label=False)
        chatbot = gr.Chatbot()
        user_input = gr.Textbox(lines=1, placeholder="Question", show_label=False)
        user_input.submit(
            chat,
            [conversation_id, user_input],
            [chatbot, user_input],
        )
        button = gr.Button("Reset", label="Reset", show_label=False)
        button.click(reset_chat, [], [chatbot, conversation_id])

if __name__ == "__main__":
    demo.launch(enable_queue=True, debug=True)
