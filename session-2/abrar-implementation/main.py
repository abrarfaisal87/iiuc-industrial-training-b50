from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from routes import news,summary


app = FastAPI()

app.include_router(news.router)
app.include_router(summary.router)




@app.get("/")
def read_root():
    return {"welcome to News Summerizer"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)
