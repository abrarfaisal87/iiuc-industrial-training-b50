from fastapi import FastAPI,APIRouter
import uvicorn
from pydantic import BaseModel


router = APIRouter(
    prefix="/news",
    tags=["news"]
)

class news_item(BaseModel):
    title: str
    content:str|None=None
    author: str
    
news = {
    1: {
        "id": 1,
        "title": "AI Revolution in 2025",
        "content": "AI continues to transform industries with new breakthroughs in machine learning and automation.",
        "author": "Aisha"
    },
    2: {
        "id": 2,
        "title": "Quantum Computing Advances",
        "content": "Recent developments in quantum computing are pushing the boundaries of what's possible in tech.",
        "author": "Bilal"
    },
    3: {
        "id": 3,
        "title": "SpaceX Mars Mission Update",
        "content": "SpaceX announces major milestones in their mission to send humans to Mars by the 2030s.",
        "author": "Zara"
    },
    4: {
        "id": 4,
        "title": "Renewable Energy Trends",
        "content": "A deep dive into how renewable energy sources are shaping the future of global energy consumption.",
        "author": "Omar"
    },
}


@router.get("/")
def all_news():
    return news

@router.get("/id/{id}")
def news_by_id(id: int):
    if id not in news:
        return {"error": f"news with id {id} not found"}
    return news[id]

@router.get("/author/{author}")
def news_by_author(author: str):
    author_news = [item for item in news.values() if item["author"].lower() == author.lower()]
    return author_news

@router.get("/search")
def search_news(author: str | None = None, title: str | None = None):
    filtered_news = news.values()
    
    if author:
        filtered_news = [
            item for item in filtered_news 
            if item["author"].lower() == author.lower()
        ]
    
    if title:
        filtered_news = [
            item for item in filtered_news 
            if title.lower() in item["title"].lower()
        ]
    
    return filtered_news

@router.post("/create-news")
def create_new(response_news: news_item):
    print(response_news)

    id=max(news.keys())+1
    news[id]= {
        "id":id,
        "title":response_news.title,
        "content":response_news.content,
        "author":response_news.author
    }
    return news[id]