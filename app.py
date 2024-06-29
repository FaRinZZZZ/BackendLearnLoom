from fastapi import FastAPI
from pydantic import BaseModel
from Typhoon import getNodeFromPDF
from PDFExtract import pdfExtract

class Item(BaseModel):
    pdf: str

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