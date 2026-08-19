import sqlite3
import os
from omdb_api import search_movie

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
DATABASE_NAME = os.path.join(DATABASE_DIR, "watchlist.db")

def get_connection():
    os.makedirs(DATABASE_DIR, exist_ok=True)
    connection = sqlite3.connect(DATABASE_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def add_movie(imdb_id, title, release_date, runtime, rating, overview):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
                   INSERT OR IGNORE INTO movies (imdb_id, title, release_date, runtime, rating, overview)
                   VALUES (?, ?, ?, ?, ?, ?)
                   """, (imdb_id, title, release_date, runtime, rating, overview))
    connection.commit()
    connection.close()
    print("Movie added successfully!")

def _fetch_and_save_genres(movie_id, imdb_id):
    load_dotenv()
    API_KEY = os.getenv("OMDB_API_KEY")
    BASE_URL = "http://www.omdbapi.com/"
    params = {"apikey": API_KEY, "i": imdb_id}
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("Genre"):
                genres = [g.strip() for g in data["Genre"].split(",")]
                for genre in genres:
                    add_genre_to_movie(movie_id, genre)
    except:
        pass

def add_genre(genre_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO genres (name) VALUES (?)", (genre_name,))
    conn.commit()
    conn.close()

def get_genre_id(genre_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM genres WHERE name = ?", (genre_name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def add_genre_to_movie(movie_id, genre_name):
    add_genre(genre_name)
    genre_id = get_genre_id(genre_name)
    if not genre_id:
        return
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO movie_genres (movie_id, genre_id) VALUES (?, ?)", (movie_id, genre_id))
    conn.commit()
    conn.close()

def get_movies():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, imdb_id, title, release_date, runtime, rating FROM movies")
    movies = cursor.fetchall()
    connection.close()
    return movies

def update_movie_rating(movie_id, new_rating):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE movies SET rating = ? WHERE id = ?", (new_rating, movie_id))
    connection.commit()
    connection.close()
    print("Movie rating updated successfully!")

def delete_movie(movie_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
    connection.commit()
    connection.close()
    print("Movie deleted successfully!")

def get_movie_by_title(title):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, imdb_id, title, release_date, runtime, rating FROM movies WHERE title = ?", (title,))
    movie = cursor.fetchone()
    connection.close()
    return movie

def add_movies_batch(titles):
    from omdb_api import search_movie
    added = []
    failed = []
    for title in titles:
        movie_data = search_movie(title)
        if not movie_data:
            failed.append(title)
            continue
        add_movie(movie_data["imdb_id"], movie_data["title"], movie_data["release_date"], movie_data["runtime"], movie_data["rating"], movie_data["overview"])
        added.append(movie_data["title"])
    return {"added": added, "failed": failed}

def update_movie_status(movie_id, new_status):
    valid_statuses = ("want_to_watch", "watching", "watched")
    if new_status not in valid_statuses:
        print(f"Error: invalid status '{new_status}'. Must be one of {valid_statuses}.")
        return
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM watchlist WHERE movie_id = ?", (movie_id,))
    existing = cursor.fetchone()
    if existing:
        cursor.execute("UPDATE watchlist SET status = ? WHERE movie_id = ?", (new_status, movie_id))
    else:
        cursor.execute("INSERT INTO watchlist (movie_id, status) VALUES (?, ?)", (movie_id, new_status))
    connection.commit()
    connection.close()
    print("Movie status updated successfully!")

def get_movies_by_status(status):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT movies.id, movies.imdb_id, movies.title, movies.release_date, movies.runtime, movies.rating, watchlist.status
                   FROM movies JOIN watchlist ON movies.id = watchlist.movie_id
                   WHERE watchlist.status = ?
                   """, (status,))
    movies = cursor.fetchall()
    connection.close()
    return movies

def get_movie_by_id(movie_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, title FROM movies WHERE id = ?", (movie_id,))
    movie = cursor.fetchone()
    connection.close()
    return movie

def get_movie_by_imdb_id(imdb_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, title FROM movies WHERE imdb_id = ?", (imdb_id,))
    movie = cursor.fetchone()
    connection.close()
    return movie

def find_movies_by_title(title):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, title, imdb_id FROM movies WHERE LOWER(title) LIKE ?", (f"%{title.lower()}%",))
    movies = cursor.fetchall()
    connection.close()
    return movies

def get_movie_by_exact_title(title):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, title, imdb_id FROM movies WHERE LOWER(title) = ?", (title.lower(),))
    movie = cursor.fetchone()
    connection.close()
    return movie

def find_movies_by_title(title):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, title, imdb_id FROM movies WHERE LOWER(title) LIKE ?", (f"%{title.lower()}%",))
    movies = cursor.fetchall()
    connection.close()
    return movies
from movie_list import POPULAR_MOVIES
import time

def import_500_movies(delay=0.5):
    added = 0
    failed = 0

    for i, title in enumerate(POPULAR_MOVIES, 1):
        print(f"[{i}/{len(POPULAR_MOVIES)}] Processing: {title}")
        data = search_movie(title)

        if data:
            add_movie(
                imdb_id=data.get("imdb_id"),
                title=data.get("title"),
                release_date=data.get("release_date"),
                runtime=data.get("runtime"),
                rating=data.get("rating"),
                overview=data.get("overview")
            )

            movie = get_movie_by_title(data.get("title"))
            if movie:
                update_movie_status(movie[0], "want_to_watch")

            added += 1
            print(f"Added: {data.get('title')}")
        else:
            failed += 1
            print(f"Failed: {title}")

        time.sleep(delay)

    print(f"\nImport complete")
    print(f"Added: {added}")
    print(f"Failed: {failed}")