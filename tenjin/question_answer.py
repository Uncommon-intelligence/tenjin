import os
import uuid
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
Your job is to summarize the the data that is returned from a resource.
Be verbose and include as much information as possible. in less that 1000 characters.
If there is nothing to summarize respond with NONE. In your response, prioritize the most recent information.


Summarize the following:
[START SUMMARIES]
{summaries}
[END SUMMARIES]


SUMMARY: [Write your summary here]
"""

PROMPT = PromptTemplate(template=template, input_variables=["summaries"])

chat_template = """
Today's date is Feb 23rd 2023

Arti is designed to be a research assistent able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Arti is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
Arti is able use external resourcecs to provide more context to the conversation. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Arti is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
The answers to questions should be given as a formal statement in markdown format. Code, should be written in markdown format with the appropriate language identifier. For example, to write a python code block, use the following syntax:
If you do not know the answer, respond with I don't know.

```python

```

Prior to answering the question research was conducted and the followin infomation was found:
RESEARCH:
{research}

The following is the last few messages in the conversation:
HISTORY:
{history}

Human: {question}
Assistant:"""

PROMPT2 = PromptTemplate(
    template=chat_template, input_variables=["research", "history", "question"]
)


def load_research_chain(query: str) -> Tuple[LLMChain, List[Document]]:
    conductor = Conductor(llm=llm)
    func = conductor.route(query)
    docs = func(query) if func else []

    return (
        load_qa_with_sources_chain(
            llm, chain_type="stuff", verbose=True, prompt=PROMPT, output_key="research"
        ),
        docs,
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
            llm=llm, prompt=PROMPT2, verbose=True, output_key="response", memory=memory
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
    research_chain, docs = load_research_chain(query)
    conversation_chain, history, buffer = load_conversation_chain(conversation_id)

    chain = SequentialChain(
        chains=[research_chain, conversation_chain],
        input_variables=["input_documents", "question", "history"],
        output_variables=["research", "response"],
        verbose=True,
    )

    output = chain({"input_documents": docs, "question": query, "history": ""})
    buffer.append(conversation_chain.memory.buffer[-1])

    # Convert input documents to a dict so that it can be serialized to json.
    output["input_documents"] = [
        doc.dict() for doc in output.get("input_documents", [])
    ]

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
