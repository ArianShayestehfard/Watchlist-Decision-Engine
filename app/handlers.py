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

def view_watchlist_handler():
    status = get_valid_status("Enter status (want_to_watch, watching, watched): ")
    movies = get_movies_by_status(status)
    if not movies:
        print(f"No movies with status '{status}'.")
        return
    for movie in movies:
        print(f"Title: {movie[2]}, Rating: {movie[5]}, Status: {movie[6]}")

def add_movie_handler():
    title = input("Enter movie title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    existing = get_movie_by_exact_title(title)
    if existing:
        print(f"Movie '{existing[1]}' already exists in database.")
        confirm = input("Do you want to add it to your watchlist? (y/n): ").lower()
        if confirm == 'y':
            update_movie_status(existing[0], "want_to_watch")
            print("Movie added to watchlist with status 'want_to_watch'.")
        else:
            print("Operation cancelled.")
        return
    data = search_movie(title)
    if not data:
        return
    add_movie(data["imdb_id"], data["title"], data["release_date"], data["runtime"], data["rating"], data["overview"])
    movie = get_movie_by_title(data["title"])
    if movie:
        update_movie_status(movie[0], "want_to_watch")
        print("Movie added to watchlist with status 'want_to_watch'.")

def change_status_handler():
    movie = select_movie_by_title("Enter movie title: ")
    if not movie:
        return
    print(f"Selected movie: {movie[1]}")
    status = get_valid_status("Enter new status (want_to_watch, watching, watched): ")
    update_movie_status(movie[0], status)

def rate_movie_handler():
    movie = select_movie_by_title("Enter movie title: ")
    if not movie:
        return
    print(f"Selected movie: {movie[1]}")
    rating = get_valid_rating("Enter your rating (0-10): ")
    update_movie_rating(movie[0], rating)

def recommend_movie_handler():
    rec = recommend_movie()
    if rec:
        print(f"Recommended: {rec[2]} (IMDB rating: {rec[5]})")
    else:
        print("No rated movies in your watchlist.")


