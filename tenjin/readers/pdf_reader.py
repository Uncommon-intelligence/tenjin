import os
import fitz
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import Callable

page_break = "\n---PAGE BREAK---\n"


class PDFReader:
    """
    PDF Reader

    allows for extracting text from a pdf file and parsing it for citations.
    """

    def __init__(self, file, index_name: str = None):
        """
        Opens the pdf file and extracts the text

        Args:
            file (str): path to the pdf file
        """
        pdf = fitz.open(file)
        self.filename = os.path.basename(file.name)
        self.index_name = index_name or self.filename
        self.text = ""

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=50,
            length_function=len,
        )

        for page in pdf:
            text = page.get_text()
            text = re.sub(r"<EOS>|<pad>|-", "", text)
            text = re.sub(r"\s+", " ", text)
            self.text += text

    def get_text(self):
        """
        Returns the text of the pdf

        Returns:
            str : the text of the pdf
        """
        texts = self.text_splitter.split_text(self.text)
        return texts

    def store_embeddings(self, vectorstore: Callable, batch_size: int = None):
        """
        Stores the embeddings of the pdf in the vectorstore

        Args:
            vectorstore (Callable): vectorstore to store the embeddings in
            batch_size (int): batch size to use when storing the embeddings

        Returns:
            None
        """
        texts = self.get_text()
        batch_size = batch_size or 200

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            print("processing ", self.filename)

            vectorstore.add_texts(batch, namespace=self.index_name)
