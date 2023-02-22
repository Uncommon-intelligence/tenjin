import os
import uuid
import tenjin.config
from typing import List, Union, Callable
from dotenv import load_dotenv
from langchain import OpenAI, PromptTemplate
from tenjin.utils.storage import store_conversation_data, fetch_conversation_data
from langchain.prompts import PromptTemplate
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.docstore.document import Document
from langchain.chains import LLMChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

llm = OpenAI(
    temperature=0,
    max_tokens=1000,
    model_name="text-davinci-003",
)

search = GoogleSearchAPIWrapper()



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

websearch_template = """
Based on the following requests, parse out the information where a Google search may be required.
If the query is based on a timeframe, assume the current date is February 22, 2023 unless otherwise specified.
If you think that you can answer the question without a Google search, respond with NONE.
Write the query, and respond with ONLY the query you would submit to Google. do not include quotation marks.

{query}

QUERY: [Write your query here]
"""

SEARCH_PROMPT = PromptTemplate(template=websearch_template, input_variables=["query"])



def get_web_results(query: str) -> List[dict]:
    chain = LLMChain(llm=llm, prompt=SEARCH_PROMPT)
    search_term = chain.run(query)

    if search_term == "NONE":
        return []

    results = search.results(search_term, 10)
    sources = []

    for result in results:
        sources.append(Document(
            page_content=result["snippet"],
            metadata={
                "type": "Google Search",
                "term": search_term,
                "source": result["link"],
                "title": result["title"],
                "content": result["snippet"],
            },
        ))

    search_index = FAISS.from_documents(sources, OpenAIEmbeddings())
    return search_index.similarity_search(search_term, k=3)

def placeholder(query: str) -> List[dict]:
    return []

TOOLS = [
    {
        "name": "Google Search",
        "description": "Useful for when you need to answer questions about current events. You should ask targeted questions",
        "command": get_web_results,
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
    web = get_web_results(query)
    chain = load_qa_with_sources_chain(llm, chain_type="stuff", verbose=True, prompt=PROMPT)
    output = chain({"input_documents": docs, "question": query})
    # tool = determine_the_proper_tool(query)

    return output, tool
