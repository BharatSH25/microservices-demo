# m2/app/main.py

from fastapi import FastAPI
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

class Message(BaseModel):
    message: str

@app.post("/process")
async def process_message(payload: Message):
    logging.info(f"Received message: {payload.message}")
    return {"status": "processed"}
