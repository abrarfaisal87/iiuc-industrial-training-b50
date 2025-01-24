#  Contains the Create, Read, Update, and Delete (CRUD) operations.
#  These functions interact with the database models using SQLAlchemy ORM.
from sqlalchemy.orm import Session
from . import models, schemas

#get all the news
def getNews(db:Session,newsId:int):
    return db.query(models.News).filter(models.News.id == newsId).first()

#get the list of news
def getNewsList(db:Session,skip:int = 0, limit:int = 10):
    print(db,skip,limit)
    return db.query(models.News).order_by(models.News.datetime.desc()).offset(skip).limit(limit).all()

#create of get the existing catergory
def getOrCreateCategory(db:Session,name:str,description:str):
    category = db.query(models.Category).filter(models.Category.name == name).first()
    if  category is None:
        category = models.Category(name=name,description=description)
        db.add(category)
        db.commit()
        db.refresh(category)
    return category

#create or get the existing reporter info
def getOrCreateReporter(db: Session, name: str, email: str):
    reporter = db.query(models.Reporter).filter(models.Reporter.name == name).first()
    if reporter is None:
        reporter = models.Reporter(name=name, email=email)
        db.add(reporter)
        db.commit()
        db.refresh(reporter)
    return reporter 

# to see publisher is there or create new
def getOrCreatePublisher(db: Session, name: str, website: str):
    publisher = db.query(models.Publisher).filter(models.Publisher.name == name).first()
    if publisher is None:
        publisher = models.Publisher(name=name, website=website)
        db.add(publisher)
        db.commit()
        db.refresh(publisher)
    return publisher

#to see if the desired news is there or not
def getNewsExistance(db:Session,newsTitle:str):
    return db.query(models.News).filter(models.News.title == newsTitle ).first()

def createImage(db: Session, newsId: int, url: str):
    dbImage = models.Image(  news_id=newsId, url=url)
    db.add(dbImage)
    db.commit()
    db.refresh(dbImage)
    return dbImage

def createNews(db:Session,news:schemas.NewsCreate):
    category = getOrCreateCategory(db, news.news_category, f"{news.news_category} description")
    reporter = getOrCreateReporter(db, news.news_reporter, f"{news.news_reporter}@example.com")
    
    publisher = getOrCreatePublisher(db, news.news_publisher, f"http://{news.publisher_website}")
    newsExist = getNewsExistance(db,newsTitle=news.title)
    
    print(category.name,reporter.name,publisher.name)
    if newsExist:
        return newsExist
    
    dbNews = models.News(
        title = news.title,
        datetime = news.datetime,
        body = news.body,
        link = news.link,
        category_id = category.id,
        reporter_id = reporter.id,
        publisher_id = publisher.id
    )
    print(dbNews)
    db.add(dbNews)
    db.commit()
    db.refresh(dbNews)
    
    for imageUrl in news.images:
        createImage(db, newsId=dbNews.id,url=imageUrl)
    return dbNews

#summarizatin of news
def insert_summary(db: Session, news_id: int, summary_text: str):
    db_summary = models.Summary(news_id=news_id, summary_text=summary_text)
    db.add(db_summary)
    db.commit()
    db.refresh(db_summary)
    return db_summary


def get_summary(db: Session, summary_id: int):
    return db.query(models.Summary).filter(models.Summary.id == summary_id).first()
