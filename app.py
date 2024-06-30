from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Typhoon import getNodeFromPDF, getFlashCard, getAiSummary
from PDFExtract import pdfExtract

class Topic(BaseModel):
    topic: str

class QA(BaseModel):
    topic: str
    n: int

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/ping')
async def show():
    return {"pong": "pong"}

@app.get('/')
async def genNode():
    pdf_path = "temp.pdf"
    pdf = pdfExtract(pdf_path)
    return getNodeFromPDF(pdf)

@app.post('/getNode')
async def getNode(file: UploadFile):
    try:
        file_path = "temp.pdf"
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        print("File saved successfully")
        pdf = pdfExtract(file_path)
        print("sending back response")
        return getNodeFromPDF(pdf)
    except Exception as e:
        print(e)
        return {"message": e.args}

@app.get('/getFlashCards/{topic}')
async def getFlashCards(topic):
    res = getFlashCard(topic)
    return res

@app.get('/getSummary/{topic}')
async def getSummary(topic):
    res = getAiSummary(topic)
    return res

if __name__ == "__main__":
    pdf_path = "3.pdf"
    pdf = pdfExtract(pdf_path)
    print(getNodeFromPDF(pdf))