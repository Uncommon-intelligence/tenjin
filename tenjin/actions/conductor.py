from typing import Tuple, List

from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAIChat
from tenjin.actions.bing_search import BingSearch


def placeholder(query: str) -> List[dict]:
    return []

bing = BingSearch()
llm = OpenAIChat(temperature=0)
tools = [
    Tool(
        name = bing.name,
        description = bing.description,
        func=bing.run
    ),
]

class Conductor:
    def run(self, query: str) -> Tuple[str, List[dict]]:
        agent = initialize_agent(tools=tools, llm=llm, agent="zero-shot-react-description", verbose=True, return_intermediate_steps=True)
        response = agent({"input", query})
        output = response.get("output", "")

        sources = bing.sources(query)

        return output, sources
