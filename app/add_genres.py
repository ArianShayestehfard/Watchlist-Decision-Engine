from movie_service import get_movies, get_movie_by_id
from omdb_api import search_movie
from database import get_connection

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


