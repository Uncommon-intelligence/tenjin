import pinecone
from hashlib import sha256

class PineconeConnector:
    """
    The Pinecone Connector allows you to connect to a Pinecone Index and upsert
    data into it and perform queries.
    """
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

    def upsert(self, ids, embeds, meta, namespace="default"):
        """
        upsert data into pinecone

        args:
            ids: list of ids
            embeds: list of embeddings
            meta: list of metadata
            namespace: pinecone namespace
        
        """

        data = zip(ids, embeds, meta)
        data = list(data)
        batch_size = 200

        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            self.index.upsert(batch, namespace=namespace)

    def query(self, embed, top_k=10, namespace="default"):
        """
        query pinecone

        args:
            embed: embedding
            top_k: number of results to return
        """
        return self.index.query(embed, top_k=top_k, include_metadata=True, namespace=namespace)