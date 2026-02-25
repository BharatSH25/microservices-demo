# m1/app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os

app = FastAPI()

M2_URL = os.getenv("M2_URL", "http://localhost:8001/process")

class Message(BaseModel):
    message: str

@app.post("/send")
async def send_message(payload: Message):
    timeout = httpx.Timeout(10.0, connect=3.0)
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(M2_URL, json=payload.model_dump())
            response.raise_for_status()
        return {"m2_response": response.json()}
    except httpx.ConnectTimeout:
        raise HTTPException(status_code=504, detail=f"Timeout connecting to M2 at {M2_URL}")
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Error reaching M2 at {M2_URL}: {exc}") from exc
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"M2 returned status {exc.response.status_code}: {exc.response.text}",
        ) from exc
