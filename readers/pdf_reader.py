import fitz
import re

page_break = '\n---PAGE BREAK---\n'

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
        self.text = ''

        for page in pdf:
            text = page.get_text()

            text = re.sub(r'<EOS>|<pad>|-', '', text)
            text = re.sub(r'\s+',' ',text)

            self.text += text
            self.text += page_break

    def get_text(self):
        """
        Returns the text of the pdf

        Returns:
            str : the text of the pdf
        """
        return self.text

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
        citations = re.findall(r'\[([\d]*)\].*?\.(.*?)\.', self.text)

        return citations