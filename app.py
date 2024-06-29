from fastapi import FastAPI
from pydantic import BaseModel
from Typhoon import getNodeFromPDF, getFlashCard
from PDFExtract import pdfExtract

class Item(BaseModel):
    pdf: str

class QA(BaseModel):
    topic: str
    n: int

app = FastAPI()

@app.get('/')
async def genNode():
    pdf_path = "1.pdf"
    pdf = pdfExtract(pdf_path)
    return getNodeFromPDF(pdf)

@app.post('/getNode')
async def getNode(item: Item):
    res = getNodeFromPDF(item.pdf)
    return res

@app.post('/getFlashCards')
async def getFlashCards(qa: QA):
    res = getFlashCard(qa.topic, qa.n)
    return res