from typing import List, Tuple

from langchain import PromptTemplate
from langchain.llms import OpenAIChat
from langchain.chains import LLMChain

from tenjin.actions import Conductor
from tenjin.utils.storage import fetch_conversation_data, store_conversation_data
from tenjin.actions.conductor import AVAILABLE_TOOLS

llm = OpenAIChat(temperature=0)

template = """
Today's date is March 8th, 2023.

You are a research companion that is skilled at helping users find the answers to they're questions.
Besides the information you have store in your memory, you can also communicate with an agent that
has access to many different sources of information.

The agent is able to answer questions using the following tools:
{tools}

To make sure that the agent knows what you need help with, you can pull information from the
conversation that you are having with the user.

CHAT HISTORY:
{history}


If you are unable to answer a question or you are asked a question that is about a current events
you can ask the agent for help. To do so, simply respond with the following:

```
<|AGENT|> [QUERY]
```


User: {question}
Assistant:
"""


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

    history, buffer = load_conversation_chain(conversation_id)

    # TODO: This should be made into a custom memory module
    chat_history = ""
    for message in buffer:
        if message["role"] != "system":
            chat_history += f"{message['role'].capitalize()}: {message['content']}\n"

    prompt = PromptTemplate(template=template, input_variables=["question", "tools", "history"])
    llm = OpenAIChat(temperature=0, prefix_messages=buffer)
    chain = LLMChain(prompt=prompt, llm=llm)
    result = chain({"question": query, "tools": AVAILABLE_TOOLS, "history": chat_history})
    output = result["text"]

    sources = []

    if "<|AGENT|>" in output:
        search_term = output.replace("<|AGENT|>", "").strip()
        output, sources = Conductor().run(search_term)
        context = "".join([source.get("snippet", "") for source in sources])

        buffer.append({"role": "system", "content": context})

    buffer.append({"role": "user", "content": query})
    buffer.append({"role": "assistant", "content": output})
    history.append({ "user": query, "assistant": output, "sources": sources})

    store_conversation_data(file_name=conversation_id, payload={
        "history": history,
        "buffer": buffer,
    })

    return history
