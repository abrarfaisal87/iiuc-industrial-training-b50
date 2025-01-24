from database import Base,engine
from models import news,Publisher,Category,Reporter,Image,Summary

Base.metadata.create_all(bind=engine)
print("All tables created successfully!")