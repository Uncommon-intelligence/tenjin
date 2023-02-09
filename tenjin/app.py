# NOTE: It looks like the chat history is being stored as an array of strings. This should be able to be serialized to JSON and stored in a database.
import toml
import openai
import gradio as gr
import pinecone
import uuid

from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings

from readers.pdf_reader import PDFReader
from chat_templates.books import book_prompt

with open("config.toml") as f:
    config = toml.load(f)

openai.api_key = config["openai"]["api_key"]

openai_api_key = config["openai"]["api_key"]
embedding_model = config["openai"]["embedding_model"]

pinecone_api_key = config["pinecone"]["api_key"]
pinecone_index_name = config["pinecone"]["index_name"]
pinecone_environment = config["pinecone"]["environment"]

pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)

llm = OpenAI(
    openai_api_key=openai_api_key,
    temperature=0,
    max_tokens=500,
    model_name="text-davinci-003",
)

index = pinecone.Index("tenjin")
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
vectorstore = Pinecone(index, embeddings.embed_query, "text")


def vectorize_file(file, index_name:str=None):
    reader = PDFReader(file, index_name=index_name)
    reader.store_embeddings(vectorstore)

    return reader.filename

def vectorise_files(files):
    # generate a uuid for the index name
    index_name = str(uuid.uuid4())

    for file in files:
        vectorize_file(file, index_name=index_name)

    print('done')
    return index_name, "✔️ Upload completed"


def ask_question(question, history, filename, memory=None):
    filename = filename or "MEDITATIONS Marcus Aurelius 6x9pdfiknh1h__.pdf"
    history = history or []
    buffer = memory.buffer if memory else []
    prompt, _memory = book_prompt(buffer=buffer)
    memory = memory or _memory  # NOTE: This is where the memory is being stored

    chain = load_qa_chain(llm, chain_type="stuff", memory=memory, prompt=prompt)
    docs = vectorstore.similarity_search(question, namespace=filename, k=4)

    output = chain(
        {"input_documents": docs, "question": question}, return_only_outputs=True
    )

    answer = output["output_text"]

    ## Store this in a database
    memory.buffer

    history.append((question, answer))
    return history, history, "", memory


with gr.Blocks() as demo:
    filename = gr.State()

    with gr.Tab("Documents"):
        files = gr.Files(file_count="multiple", file_types=["pdf"])
        status = gr.Markdown()
        files.upload(vectorise_files, files,  [filename, status])

    with gr.Tab("Chat"):
        memory = gr.State()
        state = gr.State()
        chatbot = gr.Chatbot()
        user_input = gr.Textbox(lines=1, placeholder="Question", show_label=False)
        user_input.submit(
            ask_question,
            [user_input, state, filename, memory],
            [chatbot, state, user_input, memory],
        )


if __name__ == "__main__":
    demo.launch(enable_queue=True, debug=True)
