from typing import List, Tuple

from langchain import PromptTemplate
from langchain.llms import OpenAIChat
from langchain.chains import LLMChain

from tenjin.actions import Conductor
from tenjin.utils.storage import fetch_conversation_data, store_conversation_data

llm = OpenAIChat(temperature=0)

prefix_content = """
IMPORTANT: If you are asked a question that you do not know the answer to or you're
unable to answer, respond with the following:

```
AGENT:
[description of the question and any information you have about it]
```

Your name is Arti. Today's date is March 8th, 2023.

Arti is designed to be a research assistant able to assist with a wide range of tasks,
from answering simple questions to providing in-depth explanations and discussions on a
wide range of topics. As a language model, Arti is able to generate human-like text
based on the input it receives, allowing it to engage in natural-sounding conversations
and provide responses that are coherent and relevant to the topic at hand.

Arti is able use external resources to provide more context to the conversation. It is
able to process and understand large amounts of text, and can use this knowledge to
provide accurate and informative responses to a wide range of questions. Additionally,
Arti is able to generate its own text based on the input it receives, allowing it to
engage in discussions and provide explanations and descriptions on a wide range of
topics.

Your response must always be in markdown format.

Code, should be written in markdown format with the appropriate language identifier.
For example, to write a python code block, use the following syntax:


```python

```
"""

prefix_messages = [{
    "role": "system",
    "content": prefix_content,
}]


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

    return history, buffer


def run(conversation_id: str, query: str) -> dict:
    """Invoke a conversation by routing the provided query to the appropriate
    transformer chains and storing the conversation history using the
    ConversationBufferMemory class.

    Args:
        query (str): The question or statement provided by the user.

    Returns:
        dict: The output of the transformer chain.
    """

    template = """
    Question: {question}

    Answer:
    """

    history, buffer = load_conversation_chain(conversation_id)

    if (len(buffer) == 0):
        buffer = prefix_messages

    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm = OpenAIChat(temperature=0, prefix_messages=buffer)
    chain = LLMChain(prompt=prompt, llm=llm)
    output = chain.run(query)
    sources = []

    if "AGENT" in output:
        output, sources = Conductor().run(query)


    buffer.append({"role": "user", "content": query})
    buffer.append({"role": "assistant", "content": output})

    history.append({
        "user": query,
        "assistant": output,
        "sources": sources,
    })

    # Save the conversation history to the S3
    store_conversation_data(file_name=conversation_id, payload={
        "history": history,
        "buffer": buffer,
    })

    return history
