import os
import uuid
from typing import Callable, List, Union
from dotenv import load_dotenv
from langchain import OpenAI, PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
import tenjin.config
from tenjin.actions import Conductor
from tenjin.utils.storage import fetch_qa_data, store_conversation_data

from langchain.chains import SequentialChain
from langchain.chains.conversation.memory import ConversationalBufferWindowMemory

llm = OpenAI(
    temperature=0,
    max_tokens=1000,
    model_name="text-davinci-003",
)

template = """
Your job is to summarize the the data that is returned from a resource.
Be verbose and include as much information as possible. in less that 1000 characters.
If no information is returned, respond with NONE.

=========
{summaries}
=========
SUMMARY: [Write your summary here]
"""

PROMPT = PromptTemplate(template=template, input_variables=["summaries"])

chat_template = """
Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
Prior to answering a question, research is performed to find the most relevant information. This research is performed using a variety of sources, including Wikipedia, Google, and other online resources. The research is then summarized and presented to you for additional context. Please use this for reference when answering the question.

RESEARCH:
{research}

HISTORY:
{history}

Human: {question}
Assistant:"""

PROMPT2 = PromptTemplate(template=chat_template, input_variables=["research", "history", "question"])

def load_research_chain(query: str) -> Union[LLMChain, List[dict]]:
    conductor = Conductor(llm=llm)
    func = conductor.route(query)
    docs = func(query) if func else []

    return load_qa_with_sources_chain(llm, chain_type="stuff", verbose=True, prompt=PROMPT, output_key="research"), docs

def load_conversation_chain(conversation_id: str) -> LLMChain:
    """loads a conversation chain using the memory buffer store on s3.

    Args:
        conversation_id (str): The id of the conversation.

    Returns:
        LLMChain: The conversation chain to use for the request
    """
    buffer = fetch_qa_data(conversation_id)

    # TODO: Vectorize the buffers and return the top 2 that are most similar to the current query.
    partial_buffer = buffer[-2:]
    memory = ConversationalBufferWindowMemory(memory_key="history", input_key="question", buffer=partial_buffer)

    return LLMChain(llm=llm, prompt=PROMPT2, verbose=True, output_key="response", memory=memory), buffer

def run(conversation_id: str, query: str) -> dict:
    """Invoike a conversation by routing the provided query to the appropriate transformer chains and storing the conversation history usin the ConversationBufferMemory class.

    Args:
        query (str): The question or statement provided by the user.

    Returns:
        dict: The output of the transformer chain.
    """
    research_chain, docs = load_research_chain(query)
    conversation_chain, buffer = load_conversation_chain(conversation_id)

    chain = SequentialChain(
        chains=[research_chain, conversation_chain],
        input_variables=["input_documents", "question", "history"],
        output_variables=["research", "response"],
        verbose=True
    )

    output = chain({"input_documents": docs, "question": query, "history": ""})
    buffer.append(conversation_chain.memory.buffer[-1])

    # save the conversation history to the S3
    store_conversation_data(file_name=conversation_id, payload={
        "buffer": buffer
    })

    return output
