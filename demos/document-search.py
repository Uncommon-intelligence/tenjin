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

from tenjin.readers.pdf_reader import PDFReader
from chat_templates.books import book_prompt

from typing import List
from langchain import PromptTemplate
from langchain.chains.conversation.memory import ConversationalBufferWindowMemory

with open("config.toml") as f:
    config = toml.load(f)

openai.api_key = config["openai"]["api_key"]

openai_api_key = config["openai"]["api_key"]
embedding_model = config["openai"]["embedding_model"]

pinecone_api_key = config["pinecone"]["api_key"]
pinecone_index_name = config["pinecone"]["index_name"]
pinecone_environment = config["pinecone"]["environment"]

pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)


def book_prompt(buffer=List[str]):
    """
    Returns a contextualized prompt for the chatbot

    Returns:
        prompt: contextualized prompt
        memory: memory to use for the chatbot
    """
    template = """
    You are a chatbot having a converesation with a human about the contents of a book or paper.
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

    memory = ConversationalBufferWindowMemory(
        memory_key="chat_history",
        input_key="question",
        buffer=buffer,
    )

    return prompt, memory


def sammy_default():
    template = """
    You're a slack bot named Sammy having a conversation with a person or group of people.
    If a question is asked that include code exapmle or a code snippet, you should respond with the relevant code snippet wrapped in markdown code blocks.

    Previous conversation history
    {chat_history}

    New Input: {input}
    {agent_scratchpad}

    Sammy:
    """

    prompt = PromptTemplate(
        input_variables=["input", "chat_history", "agent_scratchpad"],
        template=template,
    )

    return prompt

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
