from validators import get_valid_status, get_valid_rating, select_movie_by_title
from movie_service import add_movie, update_movie_status, update_movie_rating, get_movies_by_status, get_movie_by_exact_title, get_movie_by_title
from omdb_api import search_movie
from recommendation import recommend_movie
from analytics import watched_stats, top_rated

def search_movie_handler():
    title = input("Enter movie title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    result = search_movie(title)
    if result:
        print(result)

