from typing import Callable, List

from langchain.agents import Tool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from tenjin.actions.google_search import GoogleSearch

template = """
Based on the following requests, determine the proper tool to use.
If you believe that you can answer the question without using a tool, respond with NONE.
Write the name of the tool you would use. Do not include quotation marks.

--- TOOLS ---
{tools}
-------------

QUERY: {query}

TOOL: [Write the name of the tool you would use here]
"""

PROMPT = PromptTemplate(template=template, input_variables=["query", "tools"])


def placeholder(query: str) -> List[dict]:
    return []


class Conductor:
    def __init__(self, llm):
        google_search = GoogleSearch(llm=llm, k=10)

        self.llm = llm
        self.tools = [
            Tool(
                name="Google Search",
                func=google_search.run,
                description="Useful for when you need to answer questions about current events. You should ask targeted questions",
            ),
            Tool(
                name="Wolfram Alpha",
                func=placeholder,
                description="Useful for when you need to answer questions about Math, Science, Technology, Culture, Society and Everyday Life. Input should be a search query.",
            ),
            Tool(
                name="Legal Document",
                func=placeholder,
                description="Useful for when you need to answer questions about legal documents. Input should be a search query.",
            ),
        ]

    def route(self, query: str) -> Callable[[str], List[dict]]:
        tools = [f"{tool.name}: {tool.description}" for tool in self.tools]
        tools = "\n".join(tools)
        chain = LLMChain(llm=self.llm, prompt=PROMPT)
        tool_name = chain.run(query=query, tools=tools)

        for tool in self.tools:
            if tool.name == tool_name:
                return tool.func
            pass
