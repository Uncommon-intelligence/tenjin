# NOTE: It looks like the chat history is being stored as an array of strings. This should be able to be serialized to JSON and stored in a database.
# NOTE: I need to figure out a way to control costs. I think I can do this by limiting the number of documents that are searched. potentially chunking the document using LangChain's text splitting functionality.

import toml
import openai
import argparse
import gradio as gr
import pinecone

from connectors.pinecone import PineconeConnector
from readers.pdf_reader import PDFReader

from langchain import PromptTemplate, ConversationChain, LLMChain, VectorDBQA
from langchain.llms import OpenAI
from langchain.chains.conversation.memory import ConversationalBufferWindowMemory
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings

with open('config.toml') as f:
    config = toml.load(f)

openai.api_key = config['openai']['api_key']

openai_api_key = config['openai']['api_key']
embedding_model = config['openai']['embedding_model']

pinecone_api_key = config['pinecone']['api_key']
pinecone_index_name = config['pinecone']['index_name']
pinecone_environment = config['pinecone']['environment']

pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)

connector = PineconeConnector(
    api_key=pinecone_api_key,
    environment=pinecone_environment,
    index_name=pinecone_index_name,
)

llm = OpenAI(openai_api_key=openai_api_key, temperature=0, max_tokens=500, model_name="text-davinci-003")
index = pinecone.Index("tenjin")
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
vectorstore = Pinecone(index, embeddings.embed_query, "text")

def vectorize_file(file):
    pdf = PDFReader(file.name)
    texts = pdf.get_text()
    filename = file.name.removeprefix('/tmp/')

    batch_size = 200
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]

        vectorstore.add_texts(
            batch,
            namespace=filename
        )

    return filename

def ask_question(question, history, filename, memory):
    history = history or []
    docs = vectorstore.similarity_search(question, namespace=filename, k=4)

    template = """
    You are a chatbot having a converesation with a human about the contents of a PDF document.
    You should respond to the human's question with a relevant sentence from the document as if you were the author of the document.
    If there is more than one author, reply as if you were the author of the most relevant sentence.
    Answers should be written in markdown format.

    {context}

    {chat_history}
    Human: {question}
    Chatbot:
    """

    prompt = PromptTemplate(
        input_variables=["chat_history", "question", "context"],
        template=template,
    )

    memory = memory or ConversationalBufferWindowMemory(memory_key="chat_history", input_key="question") #, buffer=buffer)
    chain = load_qa_chain(llm, chain_type="stuff", memory=memory, prompt=prompt)
    output = chain({"input_documents": docs, "question": question}, return_only_outputs=True)
    answer = output['output_text']

    ## Store this in a database
    memory.buffer

    history.append((question, answer))
    return history, history, "", memory

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1):
            # file_output = gr.File()
            filename = gr.Textbox(show_label=False, interactive=False)
            upload_button = gr.UploadButton("Click to Upload a File", file_types=["pdf"], show_progress=True)
            upload_button.upload(vectorize_file, upload_button, filename)
            gr.Markdown("*Upload a PDF file to start*")

        with gr.Column(scale=4):
            memory = gr.State()
            state = gr.State()
            chatbot = gr.Chatbot()
            user_input = gr.Textbox(lines=1, placeholder="Question", show_label=False)
            user_input.submit(ask_question, [user_input, state, filename, memory], [chatbot, state, user_input, memory])

if __name__ == '__main__':
    demo.launch()
