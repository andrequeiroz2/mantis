from fastapi import FastAPI
from core.config import settings
from endpoint.user import user_router
import uvicorn
app = FastAPI()


app.include_router(user_router, tags=["User"])



if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, log_level=settings.LOGLEVEL)

