import os
from pypdf import PdfReader
from fixthaipdf import clean

def pdfExtract(pdf_path):
    reader = PdfReader(pdf_path)
    #number_of_pages = len(reader.pages)
    #print(number_of_pages)
    text='\n'.join([i.extract_text() for i in reader.pages])
    return clean(text)

if __name__ == "__main__":
    pdf_path = "1.pdf"
    print(pdfExtract(pdf_path))