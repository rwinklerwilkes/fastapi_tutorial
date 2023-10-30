import os
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, File, UploadFile
from sqlalchemy.orm import Session

from sql import crud, models, schemas
from sql.database import SessionLocal, engine
from file.file import FileHandler

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency
def get_file_handler(db: Session = Depends(get_db)):
    fh = FileHandler(db)
    try:
        yield fh
    finally:
        fh.close()

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


@app.get('/albums/artists/{artist_name}', response_model=list[schemas.ArtistAlbum])
def read_artists(artist_name: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    albums = crud.get_albums_by_artist(db, artist_name=artist_name, skip=skip, limit=limit)
    return albums

@app.post('/files/')
async def create_file(file: Annotated[bytes, File()]):
    return {'file_size': len(file)}

CHUNKSIZE = 1024*1024
MAX_NUM_MB = 100
MAX_FILESIZE = MAX_NUM_MB * CHUNKSIZE
@app.post('/uploadfile/')
async def create_upload_file(file: Annotated[UploadFile, File(description='A file read as an UploadFile')],
                             fh: FileHandler = Depends(get_file_handler)):
    try:
        new_filename = os.path.join('csv_tempdir', file.filename)
        if file.filename[-3:].lower() != 'csv':
            raise HTTPException(status_code=415, detail='File not of type CSV')
        with open(new_filename, 'wb') as f:
            filesize = 0
            while contents:= file.file.read(CHUNKSIZE):
                filesize += CHUNKSIZE
                if filesize > MAX_FILESIZE:
                    raise HTTPException(status_code=413, detail=f'File exceeds {MAX_NUM_MB} MB limit for uploads')
                f.write(contents)
    except HTTPException as h:
        raise h
    except Exception as e:
        return {'message': f'There was an error uploading the file: {str(e)}'}
    finally:
        file.file.close()

    fh.process_file(new_filename, file.filename)
    return {'filename': file.filename}

