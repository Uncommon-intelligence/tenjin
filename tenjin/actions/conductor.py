from typing import Tuple, List

from langchain.agents import Tool
from langchain.agents import initialize_agent, load_tools
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.chains import LLMChain
from langchain.llms import OpenAIChat
from langchain.prompts import PromptTemplate
from langchain.docstore.base import Document

from tenjin.actions.google_search import GoogleSearch


def placeholder(query: str) -> List[dict]:
    return []


class Conductor:
    def __init__(self):
        self.llm = OpenAIChat(temperature=0)
        google_search = GoogleSearch(llm=self.llm, k=10)

        self.tools = [
            Tool(
                name="Google Search",
                func=google_search.run,
                description="Useful for when you need to answer questions about current events. You should ask targeted questions",
            ),
            # Tool(
            #     name="Wolfram Alpha",
            #     func=placeholder,
            #     description="Useful for when you need to answer questions about Math, Science, Technology, Culture, Society and Everyday Life. Input should be a search query.",
            # ),
            # Tool(
            #     name="Legal Document",
            #     func=placeholder,
            #     description="Useful for when you need to answer questions about legal documents. Input should be a search query.",
            # ),
            Tool(
                name="Read documents",
                func=placeholder,
                description="Useful",
            ),
        ]

    def run(self, query: str) -> Tuple[str, List[Document]]:
        prompt = ZeroShotAgent.create_prompt(
            tools=self.tools,
            prefix="Answer the following questions as best you can. You have access to the following tools:",
            suffix="Begin!\n\nQuestion: {input}\nThought:{agent_scratchpad}",
            input_variables=["input", "agent_scratchpad"],
        )

        llm_chain = LLMChain(llm=self.llm, prompt=prompt)
        tool_names = [tool.name for tool in self.tools]
        agent = ZeroShotAgent(
            llm_chain=llm_chain,
            allowed_tools=tool_names,
            return_intermediate_steps=True,
            max_iterations=1,
        )
        agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent, tools=self.tools, verbose=True, return_intermediate_steps=True
        )

        response = agent_executor({"input": query})
        output = response["output"]
        steps = response["intermediate_steps"]
        sources = []

        for step in steps:
            if step[0].tool != "None":
                sources.extend(step[1])

        return output, sources
