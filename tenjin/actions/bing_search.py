from typing import List
from langchain.utilities import BingSearchAPIWrapper

class BingSearch(BingSearchAPIWrapper):
    """
    Wrapper around Bing Search API that returns a list of results, sources, and metadata.
    """

    name = "Bing Search"
    description = "Useful if you need to answer questions about current events. You should ask targeted questions."

    def sources(self, query) -> List[dict]:
        sources = super().results(query, 5)
        sources = [source for source in sources if isinstance(source, dict) and source.get("snippet")]

        return sources
