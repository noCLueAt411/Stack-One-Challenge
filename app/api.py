from fastapi import FastAPI
from pydantic import BaseModel
from utils import start_call, end_call

app = FastAPI()

class CallRequest(BaseModel):
    number: str

@app.post("/call")
async def call(request: CallRequest):
    start_call(request.number)
    return {"status": "calling", "number": request.number}

@app.post("/hangup")
async def hangup():
    end_call()
    return {"status": "call ended"}