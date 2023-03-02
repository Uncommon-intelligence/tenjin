import os
import uuid
from datetime import datetime
from typing import Callable, List, Tuple

from dotenv import load_dotenv
from langchain import PromptTemplate
from langchain.llms import OpenAIChat
from langchain.chains import LLMChain, SequentialChain
from langchain.chains.conversation.memory import ConversationalBufferWindowMemory
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.docstore.document import Document

import tenjin.config
from tenjin.actions import Conductor
from tenjin.utils.storage import fetch_conversation_data, store_conversation_data

llm = OpenAIChat(temperature=0)

prefix_content = """
Arti is designed to be a research assistent able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Arti is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
Arti is able use external resourcecs to provide more context to the conversation. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Arti is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Your response must always be in markdown format.

Code, should be written in markdown format with the appropriate language identifier. For example, to write a python code block, use the following syntax:
If you do not know the answer, respond with I don't know.

Don't return an exact copy of the research. Instead, paraphrase the information and provide a summary of the research and expand on it with additional details and examples if applicable.

```python

```
"""

prefix_messages = [{
    "role": "system",
    "content": prefix_content,
}]

# template = """
# {research}
# """

# PROMPT = PromptTemplate(
#     template=template, input_variables=["history", "question", "research"]
# )


def load_conversation_chain(
    conversation_id: str,
) -> Tuple[LLMChain, List[dict], List[str]]:
    """loads a conversation chain using the memory buffer store on s3.

    Args:
        conversation_id (str): The id of the conversation.

    Returns:
        LLMChain: The conversation chain to use for the request
    """
    history, buffer = fetch_conversation_data(conversation_id)

    return history or [], buffer or []


def run(conversation_id: str, query: str) -> dict:
    """Invoke a conversation by routing the provided query to the appropriate transformer chains and storing the conversation history usin the ConversationBufferMemory class.

    Args:
        query (str): The question or statement provided by the user.

    Returns:
        dict: The output of the transformer chain.
    """
    template = """Question: {question}

    Answer:"""

    prompt = PromptTemplate(template=template, input_variables=["question"])
    research_output, documents = Conductor().run(query)

    history, buffer = load_conversation_chain(conversation_id)

    if research_output:
        buffer.append({"role": "system", "content": research_output or ""})

    llm = OpenAIChat(temperature=0, prefix_messages=prefix_messages + buffer)
    chain = LLMChain(prompt=prompt, llm=llm)

    output = chain.run(query)

    buffer.append({"role": "user", "content": query})
    buffer.append({"role": "assistant", "content": output})

    history.append({
        "user": query,
        "assistant": output,
        "system": research_output,
        "sources": [doc.dict() for doc in documents[:5]] or [],
    })

    # Save the conversation history to the S3
    store_conversation_data(file_name=conversation_id, payload={
        "history": history,
        "buffer": buffer,
    })

    return history
