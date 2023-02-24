from langchain.chains import LLMChain
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.vectorstores.faiss import FAISS
from typing import List

search = GoogleSearchAPIWrapper()

template = """
Based on the following requests, parse out the information where a Google search may be required.
If you think that you can answer the question without a Google search, respond with NONE.
Write the query, and respond with ONLY the query you would submit to Google. do not include quotation marks.

{query}

QUERY: [Write your query here]
"""

SEARCH_PROMPT = PromptTemplate(template=template, input_variables=["query"])


class GoogleSearch:
    """
    Wrapper around Google Search API that returns a list of results, sources, and metadata.
    """

    def __init__(self, llm: LLMChain, k=10):
        self.k = k
        self.llm = llm

    def run(self, query: str) -> List[dict]:
        """run

        Args:
            query (str): English query to search for

        Returns:
            List[dict]: List of Documents including metadata
        """
        chain = LLMChain(llm=self.llm, prompt=SEARCH_PROMPT)
        search_term = chain.run(query)

        if search_term == "NONE":
            return []

        results = search.results(search_term, self.k)
        sources = []

        for result in results:
            sources.append(
                Document(
                    page_content=result["snippet"],
                    metadata={
                        "type": "Google Search",
                        "term": search_term,
                        "source": result["link"],
                        "title": result["title"],
                        "content": result["snippet"],
                    },
                )
            )

        search_index = FAISS.from_documents(sources, OpenAIEmbeddings())
        return search_index.similarity_search(search_term, k=6)
