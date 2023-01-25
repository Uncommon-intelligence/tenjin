# from py2neo import Graph, Node

# graph = Graph("bolt://localhost:7687", auth=("neo4j", "secure1111!"))

# person = Node("Person", name="Bob")
# graph.create(person)

import toml
import openai
import argparse
import gradio as gr

from hashlib import sha256
from connectors.pinecone import PineconeConnector
from readers.pdf_reader import PDFReader
from embedders.openai_embedder import OpenAIEmbedder
from gpt import GPT3

parser = argparse.ArgumentParser()
parser.add_argument('--q', type=str, help='query')

with open('config.toml') as f:
    config = toml.load(f)

openai.api_key = config['openai']['api_key']

openai_api_key = config['openai']['api_key']
embedding_model = config['openai']['embedding_model']

pinecone_api_key = config['pinecone']['api_key']
pinecone_index_name = config['pinecone']['index_name']
pinecone_environment = config['pinecone']['environment']

connector = PineconeConnector(
    api_key=pinecone_api_key,
    environment=pinecone_environment,
    index_name=pinecone_index_name,
)

embedder = OpenAIEmbedder(model=embedding_model)
gpt = GPT3()

def vectorize_file(file):
    # uploads.append(file)
    pdf = PDFReader(file.name)
    text = pdf.get_text_by_page()
    filename = file.name.removeprefix('/tmp/')

    ids, embeds, meta = embedder.create(text)
    connector.upsert(ids=ids, embeds=embeds, meta=meta, namespace=filename)

    return filename

def ask_question(question, history, filename):
    history = history or []

    _, query, _ = embedder.create(question)
    result = connector.query(embed=query[0], top_k=5, namespace=filename)
    context = [match['metadata']['text'] for match in result['matches']]
    result = gpt.query(query=question, contexts=context)
    answer = result['choices'][0]['text']

    history.append((question, answer))
    return history, history, ""

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1):
            # file_output = gr.File()
            filename = gr.Textbox(show_label=False, interactive=False)
            upload_button = gr.UploadButton("Click to Upload a File", file_types=["pdf"], show_progress=True)
            upload_button.upload(vectorize_file, upload_button, filename)
            gr.Markdown("*Upload a PDF file to start*")

        with gr.Column(scale=4):
            state = gr.State()
            chatbot = gr.Chatbot()
            user_input = gr.Textbox(lines=1, placeholder="Question", show_label=False)
            user_input.submit(ask_question, [user_input, state, filename], [chatbot, state, user_input])

if __name__ == '__main__':
    demo.launch()
