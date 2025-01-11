from fastapi import FastAPI,APIRouter

app = FastAPI()
router = APIRouter(
    prefix="/summary",
    tags=["summary"],
)

@router.get("/")
def hello():
    return {"hello"}