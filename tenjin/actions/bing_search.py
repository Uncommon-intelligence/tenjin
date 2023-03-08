from typing import List
from langchain.utilities import BingSearchAPIWrapper

class BingSearch(BingSearchAPIWrapper):
    """
    Wrapper around Bing Search API that returns a list of results, sources, and metadata.
    """

    name = "Bing Search"
    description = "Useful if you need to answer questions about current events. You should ask targeted questions."

    def sources(self, query) -> List[dict]:
        sources = []
        results = super().results(query, 5)

        for result in results:
            if result.get("snippet", "") !=  "":
                sources.append({
                    "page_content": result.get("snippet", ""),
                    "metadata": {
                        "type": "Bing Search",
                        "source": result.get("link", ""),
                        "title": result.get("title", ""),
                        "content": result.get("snippet", ""),
                    },
                })

        return sources
