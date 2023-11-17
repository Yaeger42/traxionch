from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import validators

from . import schemas, models, crud
from .database import SessionLocal, engine


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


def raise_not_found(request):
    message = f"URL {request.url}, does not exist"
    raise HTTPException(status_code=404, detail=message)


@app.get("/")
def read_root():
    return {"message": "url shortener"}


@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise raise_bad_request(message="Your provided URL is not valid")
    db_url = crud.create_db_url(db=db, url=url)
    db_url.url = db_url.key
    return db_url


@app.get("/{url_key}")
def forward_to_target_url(
    url_key: str, request: Request, db: Session = Depends(get_db)
):
    db_url = crud.get_db_url_by_key(db, url_key)
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)


@app.get("/geturlfromkey/{url_key}")
def get_url_from_key(url_key: str, request: Request, db: Session = Depends(get_db)):
    db_url = crud.get_db_url_by_key(db, url_key)
    return db_url if db_url else raise_not_found(request)
