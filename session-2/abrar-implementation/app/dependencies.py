# Contains reusable dependencies,
# such as common utility functions for dependency injection in your routes.

from .database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()