import openai

from typing import Union, List
from hashlib import sha256

class OpenAIEmbedder:
    """
    OpenAI Embedder

    Creates embeddings from text using openai's embedding api

    args:
        model: openai model name
        api_key: openai api key
    """

    def __init__(self, model, api_key):
        """
        init openai embedder

        args:
            model: openai model name
            api_key: openai api key
        """
        self.model = model
        self.api_key = api_key


    def create(self, document_text: Union[str, List[str]]):
        """
        create embeddings from list of texts
        TODO: add support for defining additional metadata

        args:
            document_text: text, list of texts

        returns:
            ids: list of ids
            embeds: list of embeddings
            meta: list of metadata
        """

        # Check if the input is a single string, if so, convert it to a list
        if isinstance(document_text, str):
            document_text = [document_text]

        # Filter out any empty strings in the list
        inputs = [text for text in document_text if len(text) > 0]

        # Hash each input text to a unique id
        ids = [sha256(i.encode('utf-8')).hexdigest()[:32] for i in inputs]

        # Create embeddings from the input texts
        embeds = openai.Embedding.create(model=self.model, input=inputs)
        embeds = [record['embedding'] for record in embeds['data']]

        # Create metadata for each text input
        meta = [{'text': text} for text in inputs]

        return ids, embeds, meta
