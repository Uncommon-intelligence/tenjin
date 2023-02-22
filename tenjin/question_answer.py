import os
import uuid
from typing import Callable, List, Union

from dotenv import load_dotenv
from langchain import OpenAI, PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.vectorstores.faiss import FAISS
from tenjin.actions import GoogleSearch

import tenjin.config
from tenjin.utils.storage import (fetch_conversation_data,
                                  store_conversation_data)

llm = OpenAI(
    temperature=0,
    max_tokens=1000,
    model_name="text-davinci-003",
)

google_search = GoogleSearch(llm=llm, k=10)

template = """
You are a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics.
Whether the human needs help with a specific question or just wants to have a conversation about a particular topic, you are here to assist.

Given the following extracted parts of a long document and a question.
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
Responses should be written in markdown format. Codeblocks should be used for code snippets and surrounded by triple backticks.
Do not include links in your response.

QUESTION: {question}
=========
{summaries}
=========
FINAL ANSWER:"""

PROMPT = PromptTemplate(template=template, input_variables=["summaries", "question"])

tool_picker_template = """
Based on the following requests, determine the proper tool to use.
If you believe that you can answer the question without using a tool, respond with NONE.
Write the name of the tool you would use. Do not include quotation marks.

--- TOOLS ---
{tools}
-------------

QUERY: {query}

TOOL: [Write the name of the tool you would use here]
"""

TOOL_PROMPT = PromptTemplate(template=tool_picker_template, input_variables=["query", "tools"])


def placeholder(query: str) -> List[dict]:
    return []

TOOLS = [
    {
        "name": "Google Search",
        "description": "Useful for when you need to answer questions about current events. You should ask targeted questions",
        "command": google_search.run,
    },
    {
        "name": "Wolfram Alpha",
        "description": "Useful for when you need to answer questions about Math, Science, Technology, Culture, Society and Everyday Life. Input should be a search query.",
        "command": placeholder,
    },
    {
        "name": "Legal Document",
        "description": "Useful for when you need to answer questions about legal documents. Input should be a search query.",
        "command": placeholder
    },
]

def determine_the_proper_tool(query: str) -> Callable[[str], List[dict]]:
    tools = [f"{tool['name']}: {tool['description']}" for tool in TOOLS]
    tools = "\n".join(tools)
    chain = LLMChain(llm=llm, prompt=TOOL_PROMPT)
    tool_name = chain.run(query=query, tools=tools)

    for tool in TOOLS:
        if tool["name"] == tool_name:
            return tool["command"]

def run(query: str) -> dict:
    tool = determine_the_proper_tool(query)
    docs = tool(query)
    chain = load_qa_with_sources_chain(llm, chain_type="stuff", verbose=True, prompt=PROMPT)
    output = chain({"input_documents": docs, "question": query})
    # tool = determine_the_proper_tool(query)

    return output, tool
