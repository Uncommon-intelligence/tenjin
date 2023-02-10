import os
import uuid
import boto3
import json
import gradio as gr
import tenjin.config
from dotenv import load_dotenv
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.agents import Tool, initialize_agent
from langchain.chains.conversation.memory import ConversationalBufferWindowMemory
from langchain.utilities import GoogleSearchAPIWrapper, WolframAlphaAPIWrapper
from tenjin.utils import date

s3_endpoint_url = os.environ.get("S3_ENDPOINT_URL")
conversation_bucket = "tenjin-conversations"

search = GoogleSearchAPIWrapper()
wolfram = WolframAlphaAPIWrapper()

s3 = boto3.client(
    "s3",
    endpoint_url=s3_endpoint_url,
)

def upload_json_to_s3(file_name: str, payload: dict):
    s3.put_object(Bucket=conversation_bucket, Key=file_name, Body=json.dumps(payload))


def fetch_conversation_data(file_name: str):
    try:
        response = s3.get_object(Bucket=conversation_bucket, Key=file_name)
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
        description="useful for when you need to answer questions about current events. You should ask targeted questions",
    ),
    Tool(
        name="Wolfram Alpha",
        func=wolfram.run,
        description=" Useful for when you need to answer questions about Math, Science, Technology, Culture, Society and Everyday Life. Input should be a search query."
    )
]

llm = OpenAI(
    temperature=0,
    max_tokens=1000,
    model_name="text-davinci-003",
)

template = f"""
Todays date: {date.today()}

Sammy is a large language model trained by OpenAI.
Sammy is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Sammy is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
Sammy is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Sammy is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
Sammy should always answer question in markdown format. If a code snippet is needed, it should be wrapped in markdown code blocks.
"""

template = template + """

TOOLS:
------

Sammy has access to the following tools:

> Google Search: useful for when you need to answer questions about current and recent events. You should ask targeted questions.
> Wolfram Alpha: Useful for when you need to answer questions about Math, Science, Technology, Culture, Society and Everyday Life. Input should be a search query.

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [Google Search, Wolfram Alpha]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
AI: [your response here]
```

Begin!

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}
"""


def load_conversation_chain(conversation_id: str):
    history, buffer = fetch_conversation_data(conversation_id)

    memory = ConversationalBufferWindowMemory(
        k=5, memory_key="chat_history", buffer=buffer
    )

    chain = initialize_agent(
        tools=tools,
        llm=llm,
        agent="conversational-react-description",
        verbose=True,
        memory=memory,
    )

    chain.agent.llm_chain.prompt.template = template

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
