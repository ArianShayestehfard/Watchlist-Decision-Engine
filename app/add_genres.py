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


