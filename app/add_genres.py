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

def update_genres_for_all_movies():
    movies = get_movies()
    for movie in movies:
        movie_id = movie[0]
        title = movie[2]
        print(f"Fetching genres for: {title}")
        data = search_movie(title)
        if data and data.get("imdb_id"):
            # از OMDb اطلاعات کامل بگیر
            import requests
            import os
            from dotenv import load_dotenv
            load_dotenv()
            API_KEY = os.getenv("OMDB_API_KEY")
            BASE_URL = "http://www.omdbapi.com/"

            params = {"apikey": API_KEY, "i": data["imdb_id"]}
            response = requests.get(BASE_URL, params=params, timeout=10)
            if response.status_code == 200:
                movie_data = response.json()
                if movie_data.get("Genre"):
                    genres = [g.strip() for g in movie_data["Genre"].split(",")]
                    for genre in genres:
                        add_genre_to_movie(movie_id, genre)
                    print(f"Added {len(genres)} genres to {title}")
        else:
            print(f"Could not fetch genres for {title}")

if __name__ == "__main__":
    update_genres_for_all_movies()
    print("Genres added successfully!")
