from fastapi import FastAPI
import uvicorn
from app.routes import news,summary
from app.database import test_connection


app = FastAPI()

app.include_router(news.router)
app.include_router(summary.router)




@app.get("/")
def read_root():
    return {"welcome to News Summerizer"}


if __name__ == "__main__":
    if test_connection():
        print("Starting the FastAPI application...")
        uvicorn.run("main:app", host="localhost", port=8001, reload=True)
    else:
        print("Failed to connect to the database. Application not starting.")
