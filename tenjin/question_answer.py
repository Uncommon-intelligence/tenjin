import os
import uuid
from typing import Callable, List, Union
from dotenv import load_dotenv
from langchain import OpenAI, PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
import tenjin.config
from tenjin.actions import Conductor

from langchain.chains import SequentialChain

llm = OpenAI(
    temperature=0,
    max_tokens=1000,
    model_name="text-davinci-003",
)

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

chat_template = """
You are a tool that converts the information provided in a summary into German.

SUMMARIES:
{research}

QUESTION: {question}
AI RESPONSE:
"""

PROMPT2 = PromptTemplate(template=chat_template, input_variables=["research", "question"])

def run(query: str) -> dict:
    conductor = Conductor(llm=llm)
    action = conductor.route(query)
    docs = action(query)
    research_chain = load_qa_with_sources_chain(llm, chain_type="stuff", verbose=True, prompt=PROMPT, output_key="research")
    chat_chain = LLMChain(llm=llm, prompt=PROMPT2, verbose=True, output_key="response")
    # output = research_chain({"input_documents": docs, "question": query})

    chain = SequentialChain(
        chains=[research_chain, chat_chain],
        input_variables=["input_documents", "question"],
        output_variables=["research", "response"],
        verbose=True
    )

    output = chain({"input_documents": docs, "question": query})

    return output
