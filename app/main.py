from database import create_tables
from movie_service import add_movie, get_movies
from omdb_api import search_movie


create_tables()

movie = search_movie("Interstellar")

if movie:

    add_movie(
        imdb_id=movie["imdb_id"],
        title=movie["title"],
        release_date=movie["release_date"],
        runtime=movie["runtime"],
        rating=movie["rating"],
        overview=movie["overview"]
    )

movies = get_movies()

for movie in movies:
    print(movie)