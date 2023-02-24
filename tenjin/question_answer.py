import os
import uuid
from datetime import datetime
from typing import Callable, List, Tuple

from dotenv import load_dotenv
from langchain import OpenAI, PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.chains.conversation.memory import ConversationalBufferWindowMemory
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.docstore.document import Document

import tenjin.config
from tenjin.actions import Conductor
from tenjin.utils.storage import fetch_conversation_data, store_conversation_data

llm = OpenAI(
    temperature=0,
    max_tokens=1000,
    model_name="text-davinci-003",
)

template = """
Arti is designed to be a research assistent able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Arti is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
Arti is able use external resourcecs to provide more context to the conversation. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Arti is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Your response must always be in markdown format.

Code, should be written in markdown format with the appropriate language identifier. For example, to write a python code block, use the following syntax:
If you do not know the answer, respond with I don't know.

Don't return an exact copy of the research. Instead, paraphrase the information and provide a summary of the research and expand on it with additional details and examples if applicable.

```python

```

Prior to answering the question research was conducted and the followin infomation was found:
RESEARCH:
{research}

The following is the last few messages in the conversation:
HISTORY:
{history}

Human: {question}
Arti:
[BEGIN MARKDOWN RESPONSE]

[YOUR RESPONSE HERE]

[END MARKDOWN RESPONSE]
"""

PROMPT = PromptTemplate(
    template=template, input_variables=["history", "question", "research"]
)


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
    history = history or []

    # TODO: Vectorize the buffers and return the top 2 that are most similar to the current query.
    partial_buffer = buffer[-2:]
    memory = ConversationalBufferWindowMemory(
        memory_key="history", input_key="question", buffer=partial_buffer
    )

    return (
        LLMChain(
            llm=llm, prompt=PROMPT, verbose=True, output_key="response", memory=memory
        ),
        history,
        buffer,
    )


def run(conversation_id: str, query: str) -> dict:
    """Invoike a conversation by routing the provided query to the appropriate transformer chains and storing the conversation history usin the ConversationBufferMemory class.

    Args:
        query (str): The question or statement provided by the user.

    Returns:
        dict: The output of the transformer chain.
    """
    research_output, documents = Conductor(llm=llm).run(query)
    chain, history, buffer = load_conversation_chain(conversation_id)

    output = chain({"question": query, "history": "", "research": research_output})
    buffer.append(chain.memory.buffer[-1])

    # Convert input documents to a dict so that it can be serialized to json.
    output["sources"] = [doc.dict() for doc in documents]

    # Add the output to the conversation history
    del output["history"]
    history.append(output)

    # save the conversation history to the S3
    store_conversation_data(
        file_name=conversation_id,
        payload={
            "buffer": buffer,  # Buffer is used to store the conversation history
            "history": history,  # History is used to store the full conversation object including sources.
        },
    )

    return history
