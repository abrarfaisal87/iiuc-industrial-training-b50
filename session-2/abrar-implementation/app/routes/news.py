from fastapi import FastAPI,APIRouter,Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from .. import crud,scrapper,dependencies,schemas,models


router = APIRouter(
    prefix="/news",
    tags=["news"]
)

# class news_item(BaseModel):
#     title: str
#     content:str|None=None
#     author: str
    
# news = {
#     1: {
#         "id": 1,
#         "title": "AI Revolution in 2025",
#         "content": "AI continues to transform industries with new breakthroughs in machine learning and automation.",
#         "author": "Aisha"
#     },
#     2: {
#         "id": 2,
#         "title": "Quantum Computing Advances",
#         "content": "Recent developments in quantum computing are pushing the boundaries of what's possible in tech.",
#         "author": "Bilal"
#     },
#     3: {
#         "id": 3,
#         "title": "SpaceX Mars Mission Update",
#         "content": "SpaceX announces major milestones in their mission to send humans to Mars by the 2030s.",
#         "author": "Zara"
#     },
#     4: {
#         "id": 4,
#         "title": "Renewable Energy Trends",
#         "content": "A deep dive into how renewable energy sources are shaping the future of global energy consumption.",
#         "author": "Omar"
#     },
# }


@router.get("/",response_model=List[schemas.News])
def read_news_list(skip:int=0,limit:int=10,db:Session = Depends(dependencies.get_db)):
    news_list = crud.getNewsList(db=db,skip=skip,limit=limit)
    if news_list is None:
        raise HTTPException(status_code=404,detail="news not found")
    return news_list

@router.get("/{news_id}", response_model=schemas.News)
def read_news(news_id: int, db: Session = Depends(dependencies.get_db)):
    news = crud.getNews(db, newsId= news_id)

    if news is None:
        raise HTTPException(status_code=404, detail="News not found")
    return news

# response_model=List[schemas.News]

@router.post("/scrape/" )
def scrape_news(urls: List[str], db: Session = Depends(dependencies.get_db)):
    """
    Scrapes news articles from a list of URLs and stores them in the database.

    Parameters:
        urls (List[str]): List of news article URLs to scrape.
        db (Session): Database session provided by dependency injection.

    Returns:
        List[schemas.News]: List of successfully inserted news objects.
    """
    all_inserted_news = []

    for url in urls:
        try:
            inserted_news = scrapper.scrape_and_store_news(url, db)
            if inserted_news:
                print(f"Successfully inserted news: {inserted_news}")  # Debugging
                all_inserted_news.append(inserted_news)
            else:
                print(f"Failed to scrape or store news for URL: {url}")
        except Exception as e:
            print(f"Error processing URL {url}: {e}")

    return all_inserted_news