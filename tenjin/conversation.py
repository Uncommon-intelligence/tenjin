import os
import uuid
import tenjin.config
from typing import List, Union
from dotenv import load_dotenv
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.agents import Tool, initialize_agent
from langchain.chains.conversation.memory import ConversationalBufferWindowMemory
from langchain.utilities import GoogleSearchAPIWrapper, WolframAlphaAPIWrapper
from tenjin.utils.storage import store_conversation_data, fetch_conversation_data

search = GoogleSearchAPIWrapper()
wolfram = WolframAlphaAPIWrapper()

tools = [
    Tool(
        name="Google Search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions",
    ),
    Tool(
        name="Wolfram Alpha",
        func=wolfram.run,
        description=" Useful for when you need to answer questions about Math, Science, Technology, Culture, Society and Everyday Life. Input should be a search query.",
    ),
]

llm = OpenAI(
    temperature=0,
    max_tokens=1000,
    model_name="text-davinci-003",
)


def load_conversation_chain(conversation_id: str):
    """
    This function initializes a chatbot's conversation chain.
    It calls relevant functions to fetch the conversation data and initialize the agent, and assigns a particular template to the chatbot's prompt.

    Parameters:

    conversation_id (str): Id of the conversation to be loaded
    Returns:

    history (obj): Fetch conversation data
    chain (obj): Chain of conversation initialized
    """
    history, buffer = fetch_conversation_data(conversation_id)
    memory = ConversationalBufferWindowMemory(
        k=5, memory_key="chat_history", buffer=buffer
    )

    chain = initialize_agent(
        tools=tools,
        llm=llm,
        agent_path="./tenjin/agents/default.json",
        verbose=True,
        memory=memory,
    )

    return history, chain


def chat(conversation_id: str, user_input: str) -> List[str]:
    """
    This function is responsible for executing a conversation chain. It takes in a conversation_id and a user_input,
    loads an existing conversation chain (or initializes a new one), gets a response from the chain and then uploads
    the response and conversation history to S3.

    Parameters:
        conversation_id (str): The conversation id.
        user_input (str): The user's input.

    Returns:
        None: This function does not return anything.
    """
    history, chain = load_conversation_chain(conversation_id)
    response = chain(user_input)

    history.append((response["input"], response["output"]))

    store_conversation_data(
        file_name=conversation_id,
        payload={
            "buffer": chain.memory.buffer,
            "history": history,
        },
    )

    return history


def reset_chat():
    """
    Resets the chatbot by generating a new conversation id.

    Args:
        None
    Returns:
        A list representing the conversation history and a new conversation id.
    """
    return [], uuid.uuid4()
