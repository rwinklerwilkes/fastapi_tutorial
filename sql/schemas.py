from pydantic import BaseModel

class AlbumBase(BaseModel):
    Title: str

class AlbumCreate(AlbumBase):
    pass

class Album(AlbumBase):
    AlbumId: int

    class Config:
        orm_mode = True

class ArtistBase(BaseModel):
    Name: str

class ArtistCreate(ArtistBase):
    pass

class Artist(ArtistBase):
    ArtistId: int
    albums: list[Album] = []

    class Config:
        orm_mode = True

class ArtistAlbum(BaseModel):
    ArtistId: int
    Name: str
    Title: str

    class Config:
        orm_mode=True