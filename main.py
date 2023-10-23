from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql import crud, models, schemas
from sql.database import SessionLocal, engine

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# https://fastapi.tiangolo.com/async/#in-a-hurry describes when to use async vs normal definitions
@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.get('/artists/', response_model=list[schemas.Artist])
def read_artists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    artists = crud.get_artists(db, skip=skip, limit=limit)
    return artists


@app.get('/artists/{artist_name}', response_model=schemas.Artist)
def read_artists(artist_name: str, db: Session = Depends(get_db)):
    artist = crud.get_artist_by_name(db, artist_name)
    return artist


@app.get('/albums/', response_model=schemas.Artist)
def read_albums(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    albums = crud.get_albums(db, skip=skip, limit=limit)
    return albums


@app.get('/albums/artists/{artist_name}', response_model=schemas.ArtistAlbum)
def read_artists(artist_name: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    albums = crud.get_albums_by_artist(db, artist_name=artist_name, skip=skip, limit=limit)
    return albums
