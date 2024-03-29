from typing import Tuple, List

from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAIChat
from tenjin.actions.bing_search import BingSearch
from langchain.utilities import WolframAlphaAPIWrapper

wolfram = WolframAlphaAPIWrapper()

bing = BingSearch()
llm = OpenAIChat(temperature=0)

TOOLS = [
    Tool(
        name = bing.name,
        description = bing.description,
        func=bing.run
    ),
    Tool(
        name ="Wolfram Alpha",
        description = "Wolfram Alpha is a computational knowledge engine that can answer questions about math, science, weather, and more.",
        func=wolfram.run
    )
]

AVAILABLE_TOOLS = " ".join([f"{tool.name}: {tool.description}\n" for tool in TOOLS])

class Conductor:
    def run(self, query: str) -> Tuple[str, List[dict]]:
        agent = initialize_agent(
            tools=TOOLS,
            llm=llm,
            agent="zero-shot-react-description",
            verbose=True,
            return_intermediate_steps=True
        )

        response = agent({"input", query})
        output = response.get("output", "")

        sources = bing.sources(query)

        return output, sources
