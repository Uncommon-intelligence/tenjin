import os
import toml
import gradio as gr
from langchain import OpenAI, LLMChain, PromptTemplate, Pinecone
from langchain.agents import Tool, initialize_agent
from langchain.chains.conversation.memory import ConversationalBufferWindowMemory, ConversationBufferMemory
from langchain.utilities import GoogleSearchAPIWrapper

with open("config.toml") as f:
    config = toml.load(f)

os.environ["OPENAI_API_KEY"] = config["openai"]["api_key"]
os.environ["GOOGLE_API_KEY"] = config["google"]["api_key"]
os.environ["GOOGLE_CSE_ID"] = config["google"]["cse_id"]

search = GoogleSearchAPIWrapper()

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

template = """
You are an AI assistant that designed to help with general tasks.

{history}
Human: {user_input}
AI: 
"""

prompt = PromptTemplate(input_variables=["history", "user_input"], template=template)

chatgpt_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=ConversationalBufferWindowMemory(k=2),
)


def chat(user_input, history, memory):
    memory = memory or ConversationalBufferWindowMemory(k=10, memory_key="chat_history")
    history = history or []
    # memory = ConversationBufferMemory(memory_key="chat_history")


    agent_chain = initialize_agent(
        tools=tools,
        llm=llm,
        agent="conversational-react-description",
        verbose=True,
        memory=memory,
    )

    # chain = LLMChain(
    #     llm=OpenAI(temperature=0),
    #     prompt=prompt,
    #     verbose=True,
    #     memory=memory,
    # )

    response = agent_chain(user_input)
    history.append((response["input"], response["output"]))

    return history, history, memory, ""


with gr.Blocks() as demo:
    with gr.Tab("Chat"):
        memory = gr.State()
        history = gr.State()
        chatbot = gr.Chatbot()
        user_input = gr.Textbox(lines=1, placeholder="Question", show_label=False)
        user_input.submit(
            chat,
            [user_input, history, memory],
            [chatbot, history, memory, user_input],
        )

if __name__ == "__main__":
    demo.launch(enable_queue=True, debug=True)
