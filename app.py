# from py2neo import Graph, Node

# graph = Graph("bolt://localhost:7687", auth=("neo4j", "secure1111!"))

# person = Node("Person", name="Bob")
# graph.create(person)

import openai
import toml

from hashlib import sha256
from connectors.pinecone import PineconeConnector
from readers.pdf_reader import PDFReader
from embedders.openai_embedder import OpenAIEmbedder

with open('config.toml') as f:
    config = toml.load(f)

openai.api_key = config['openai']['api_key']
embedding_model = config['openai']['embedding_model']

pinecone_api_key = config['pinecone']['api_key']
pinecone_index_name = config['pinecone']['index_name']
pinecone_environment = config['pinecone']['environment']

connector = PineconeConnector(
    api_key=pinecone_api_key,
    environment=pinecone_environment,
    index_name=pinecone_index_name,
)

embedder = OpenAIEmbedder(
    model=embedding_model,
    api_key=openai.api_key,
)

if __name__ == '__main__':
    pdf = PDFReader('sample.pdf')
    text = pdf.get_text_by_page()
    ids, embeds, meta = embedder.create(text)

    print(ids)

    connector.upsert(ids=ids, embeds=embeds, meta=meta)
