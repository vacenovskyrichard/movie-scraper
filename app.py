from flask import Flask, render_template, request
from data.database import db
from data.models import Actor, Movie
from utils import normalize_text
import os

app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))  # Get absolute path of app.py
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(base_dir, 'instance', 'data.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)  # Bind db to Flask app

# Ensure database tables exist before running queries
with app.app_context():
    db.create_all()


@app.route("/")
def search():
    query = request.args.get("query", "").strip()

    movies, actors = [], []

    if query:
        movies = Movie.query.filter(Movie.title_normalized.ilike(f"%{normalize_text(query)}%")).all()
        actors = Actor.query.filter(Actor.full_name_normalized.ilike(f"%{normalize_text(query)}%")).all()

    return render_template("index.html", movies=movies, actors=actors, query=query)


@app.route("/movie/<int:movie_id>")
def movie_details(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # Get the movie by its ID
    return render_template("movie_details.html", movie=movie)


@app.route("/actor/<int:actor_id>")
def actor_details(actor_id):
    actor = Actor.query.get_or_404(actor_id)  # Get the actor by their ID
    return render_template("actor_details.html", actor=actor)


if __name__ == "__main__":
    app.run(debug=True)
