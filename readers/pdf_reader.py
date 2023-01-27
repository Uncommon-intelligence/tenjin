import fitz
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

page_break = "\n---PAGE BREAK---\n"


class PDFReader:
    """
    PDF Reader

    allows for extracting text from a pdf file and parsing it for citations.
    """

    def __init__(self, file):
        """
        Opens the pdf file and extracts the text

        Args:
            file (str): path to the pdf file
        """
        pdf = fitz.open(file)
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

    def get_documents(self):
        """
        Returns the text of the pdf seperated by document

        Returns:
            list : list of strings where each string is a document of the pdf
        """
        texts = self.get_text()
        metadatas = [{"text": text} for text in texts]

        return self.text_splitter.create_documents(texts, metadatas=metadatas)

    def get_text_by_page(self):
        """
        Returns the text of the pdf seperated by page

        Returns:
            list : list of strings where each string is a page of the pdf
        """
        return self.text.split(page_break)

    def get_citations(self):
        """
        Returns all citations in the pdf

        Returns:
            list : list of tuples where each tuple contains the citation number and the text
        """
        citations = re.findall(r"\[([\d]*)\].*?\.(.*?)\.", self.text)

        return citations
