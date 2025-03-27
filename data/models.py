from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from .database import db  # Import db from database.py

# Association Table for Many-to-Many Relationship
movie_actor = Table(
    "movie_actor",
    db.metadata,  # Use db.metadata instead of Base.metadata
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
    Column("actor_id", Integer, ForeignKey("actors.id"), primary_key=True),
)


class Movie(db.Model):  # Inherit from db.Model
    __tablename__ = "movies"

    id = db.Column(Integer, primary_key=True, index=True)
    title = db.Column(String, index=True)
    title_normalized = db.Column(String)

    actors = relationship("Actor", secondary=movie_actor, back_populates="movies")


class Actor(db.Model):  # Inherit from db.Model
    __tablename__ = "actors"

    id = db.Column(Integer, primary_key=True, index=True)
    name = db.Column(String)
    surname = db.Column(String)

    full_name_normalized = db.Column(String)

    movies = relationship("Movie", secondary=movie_actor, back_populates="actors")
