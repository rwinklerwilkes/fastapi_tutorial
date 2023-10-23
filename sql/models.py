from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Artist(Base):
    __tablename__ = 'Artist'
    ArtistId = Column(Integer, primary_key=True, index=True)
    Name = Column(String, index=True)

    albums = relationship('Album', back_populates='artist')

class Album(Base):
    __tablename__ = 'Album'
    AlbumId = Column(Integer, primary_key=True, index=True)
    Title = Column(String, index=True)
    ArtistId = Column(Integer, ForeignKey('Artist.ArtistId'))

    artist = relationship('Artist', back_populates='albums')