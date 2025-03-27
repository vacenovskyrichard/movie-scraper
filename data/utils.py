import unicodedata
from flask import current_app

from app import app
from data.database import db
from data.models import Movie, Actor


def ensure_tables_exist():
    """Ensures that the tables exist in the database."""
    with current_app.app_context():
        db.create_all()


def add_movie_and_actors(movie: Movie, actors: list[Actor]):
    """Adds a movie and its actors to the database, avoiding duplicates."""
    from app import app  # Import the Flask app to get its context

    # Ensure we have an app context if calling from outside Flask
    with app.app_context():
        ensure_tables_exist()
        # Check if the movie already exists in the database
        movie_exists = Movie.query.filter(Movie.title == movie.title).first()

        if not movie_exists:
            db.session.add(movie)  # Use db.session.add instead of db.add
            db.session.commit()  # Commit to ensure movie is added and assigned an ID
            db.session.refresh(movie)  # Refresh to get the movie's ID from the DB

        else:
            movie = movie_exists  # If movie exists, use the existing one

        # Add actors to the movie's actors list
        for actor_data in actors:
            # Check if the actor already exists in the database
            actor = Actor.query.filter(Actor.name == actor_data.name, Actor.surname == actor_data.surname).first()

            if not actor:
                # Create and add the actor if it doesn't exist
                actor = Actor(name=actor_data.name,
                              surname=actor_data.surname,
                              full_name_normalized=f"{actor_data.full_name_normalized}")

                db.session.add(actor)  # Use db.session.add instead of db.add

            # Add the actor to the movie's actors list (if not already added)
            if actor not in movie.actors:
                movie.actors.append(actor)

        db.session.commit()  # Commit after adding all actors to the movie
