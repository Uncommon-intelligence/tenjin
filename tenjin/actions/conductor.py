from typing import Tuple, List

from langchain.agents import Tool
from langchain.agents import ZeroShotAgent, AgentExecutor
from langchain.chains import LLMChain
from langchain.llms import OpenAIChat
from tenjin.actions.bing_search import BingSearch


def placeholder(query: str) -> List[dict]:
    return []

bing = BingSearch()

PREFIX = """
You are a research assistant accessing data from the internet. Today is March 1st 2023.

You have access to the following tools:
"""

class Conductor:
    def __init__(self):
        self.llm = OpenAIChat(temperature=0)

        self.tools = [
            Tool(
                name = bing.name,
                description = bing.description,
                func=bing.run
            ),
        ]

    def run(self, query: str) -> Tuple[str, List[dict]]:
        prompt = ZeroShotAgent.create_prompt(
            tools=self.tools,
            prefix=PREFIX,
            suffix="Begin!\n\nQuestion: {input}\nThought:{agent_scratchpad}",
            input_variables=["input", "agent_scratchpad"],
        )

        llm_chain = LLMChain(llm=self.llm, prompt=prompt)
        tool_names = [tool.name for tool in self.tools]

        agent = ZeroShotAgent(
            llm_chain=llm_chain,
            allowed_tools=tool_names,
            return_intermediate_steps=True,
            # max_iterations=10,
        )

        agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=self.tools,
            verbose=True,
            return_intermediate_steps=True,
            max_iterations=10,
        )

        response = agent_executor({"input": query})

        output = response["output"]
        steps = response["intermediate_steps"]
        sources = bing.sources(query)

        for step in steps:
            if step[0].tool != "None":
                sources.extend(step[1])

        return output, sources
