from movie_service import get_movies, get_movie_by_id
from omdb_api import search_movie
from database import get_connection

def add_genre(genre_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO genres (name) VALUES (?)", (genre_name,))
    conn.commit()
    conn.close()

