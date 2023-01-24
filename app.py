# from py2neo import Graph, Node

# graph = Graph("bolt://localhost:7687", auth=("neo4j", "secure1111!"))

# person = Node("Person", name="Bob")
# graph.create(person)

import fitz
import re
import openai
import spacy
import toml

from hashlib import sha256
from connectors.pinecone import PineconeConnector


with open('config.toml') as f:
    config = toml.load(f)

openai.api_key = config['openai']['api_key']
embedding_model = config['openai']['embedding_model']

pinecone_api_key = config['pinecone']['api_key']
pinecone_index_name = config['pinecone']['index_name']
pinecone_environment = config['pinecone']['environment']

page_break = '\n---PAGE BREAK---\n'

nlp = spacy.load('en_core_web_sm')

class PDFReader:
    def __init__(self, file):
        pdf = fitz.open(file)
        self.text = ''

        self.connector = PineconeConnector(
            api_key = pinecone_api_key,
            environment=pinecone_environment,
            index_name=pinecone_index_name,
        )

        for page in pdf:
            text = page.get_text()

            text = re.sub(r'<EOS>|<pad>|-', '', text)
            text = re.sub(r'\s+',' ',text)

            self.text += text
            self.text += page_break

    def get_text(self):
        return self.text

    def get_citations(self):
        citations = re.findall(r'\[([\d]*)\].*?\.(.*?)\.', self.text)
        return citations

    def create_embeddings(self):
        """
        use openai's embeddings
        """
        inputs = self.text.split(page_break)
        inputs = [i for i in inputs if len(i) > 0]
        ids = [sha256(i.encode('utf-8')).hexdigest()[:32] for i in inputs]

        embeds = openai.Embedding.create(model=embedding_model, input=inputs)
        embeds = [record['embedding'] for record in embeds['data']]

        ids = [str(i) for i in range(0, len(embeds))]
        meta = [{'text': text} for text in inputs]

        self.connector.upsert(ids=ids, embeds=embeds, meta=meta)


if __name__ == '__main__':
    pdf = PDFReader('sample.pdf')
    pdf.create_embeddings()
    # print(pdf.get_citations())
