from fastapi import FastAPI
from pydantic import BaseModel
from Typhoon import getNodeFromPDF

class Item(BaseModel):
    pdf: str

app = FastAPI()

@app.post('/getNode')
async def getNode(item: Item):
    res = getNodeFromPDF(item.pdf)
    return res