from fastapi import FastAPI
from pydantic import BaseModel
from utils import start_call

app = FastAPI()

class CallRequest(BaseModel):
    number: str

@app.post("/call")
async def call(request: CallRequest):
    start_call(request.number)
    return {"status": "calling", "number": request.number}