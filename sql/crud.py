from sqlalchemy.orm import Session

from . import models, schemas

def get_artist(db: Session, artist_id: int):
    return db.query(models.Artist).filter(models.Artist.ArtistId == artist_id).first()

def get_artist_by_name(db: Session, artist_name: str):
    return db.query(models.Artist).filter(models.Artist.Name == artist_name).first()

def get_artists(db:Session, skip:int = 0, limit:int = 100):
    return db.query(models.Artist).offset(skip).limit(limit).all()

def create_artist(db:Session, artist: schemas.ArtistCreate):
    db_artist = models.Artist(Name = artist.Name)
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist

def get_albums(db:Session, skip:int = 0, limit:int = 100):
    return db.query(models.Album).offset(skip).limit(limit).all()

def get_albums_by_artist(db: Session, artist_name: str, skip:int = 0, limit:int = 100):
    q = (db.query(models.Artist, models.Album)
         .filter(models.Artist.ArtistId == models.Album.ArtistId)
         .filter(models.Artist.Name == artist_name)
         .offset(skip)
         .limit(limit).all())
    return q