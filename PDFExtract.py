import os
from pypdf import PdfReader
from fixthaipdf import clean
pdf_path = "140A022N0000000000100.pdf"
reader = PdfReader(pdf_path)
number_of_pages = len(reader.pages)
print(number_of_pages)
text='\n'.join([i.extract_text() for i in reader.pages])
print(clean(text))
print(text)