from fastapi import FastAPI
from core.config import settings
import uvicorn


app = FastAPI()


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, log_level=settings.LOGLEVEL)
