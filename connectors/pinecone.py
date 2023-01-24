import pinecone
from hashlib import sha256

class PineconeConnector:
    def __init__(self, api_key, environment, index_name="tenjin", dimension=1536):
        """
        init pinecone

        args:
            api_key: pinecone api key
            environment: pinecone environment
            index_name: pinecone index name
            dimension: embedding dimension
        """
        pinecone.init(api_key=api_key, environment=environment)
        
        if 'tenjin' not in pinecone.list_indexes():
            pinecone.create_index(index_name, dimension=dimension)

        self.index = pinecone.Index(index_name)

    def upsert(self, ids, embeds, meta):
        """
        upsert data into pinecone

        args:
            ids: list of ids
            embeds: list of embeddings
            meta: list of metadata
        
        """

        data = zip(ids, embeds, meta)
        self.index.upsert(data)
