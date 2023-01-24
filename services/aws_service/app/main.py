from fastapi import FastAPI
from core.config import settings
from endpoint.aws import aws_router
import uvicorn


app = FastAPI()

app.include_router(aws_router, tags=["AWS"], prefix="/api/awsservice")

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, log_level=settings.LOGLEVEL)
