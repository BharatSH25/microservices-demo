from fastapi import FastAPI
from pydantic import BaseModel
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class Login(BaseModel):
    username: str | None = "Bharat"
    password: str

app = FastAPI()


@app.post("/login")
async def main(req:Login):
    logger.info(" %s| %s",req.username,req.password)
    return {"success":True}