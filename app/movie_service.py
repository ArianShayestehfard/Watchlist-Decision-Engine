from database import get_connection
from omdb_api import search_movie


def add_movie(tmdb_id, title, release_date, runtime, rating, overview):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
                   INSERT OR IGNORE INTO movies (
            tmdb_id,
            title,
            release_date,
            runtime,
            rating,
            overview
        )
        VALUES (?, ?, ?, ?, ?, ?)
                   """, (
                       tmdb_id,
                       title,
                       release_date,
                       runtime,
                       rating,
                       overview
                   ))

    connection.commit()
    connection.close()

    print("Movie added successfully!")


def get_movies():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
                   SELECT id, tmdb_id, title, release_date, runtime, rating
                   FROM movies
                   """)

    movies = cursor.fetchall()

    connection.close()

    return movies


def update_movie_rating(movie_id, new_rating):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
                   UPDATE movies
                   SET rating = ?
                   WHERE id = ?
                   """, (new_rating, movie_id))

    connection.commit()
    connection.close()

    print("Movie rating updated successfully!")


def delete_movie(movie_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
                   DELETE FROM movies
                   WHERE id = ?
                   """, (movie_id,))

    connection.commit()
    connection.close()

    print("Movie deleted successfully!")


def get_movie_by_title(title):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
                   SELECT id, tmdb_id, title, release_date, runtime, rating
                   FROM movies
                   WHERE title = ?
                   """, (title,))

    movie = cursor.fetchone()

    connection.close()

    return movie


def add_movies_batch(titles):
    added = []
    failed = []

    for title in titles:
        movie_data = search_movie(title)

        if not movie_data:
            failed.append(title)
            continue

        add_movie(
            tmdb_id=movie_data["imdb_id"],
            title=movie_data["title"],
            release_date=movie_data["release_date"],
            runtime=movie_data["runtime"],
            rating=movie_data["rating"],
            overview=movie_data["overview"]
        )
        added.append(movie_data["title"])

    return {
        "added": added,
        "failed": failed
    }


def update_movie_status(movie_id, new_status):
    valid_statuses = ("want_to_watch", "watching", "watched")

    if new_status not in valid_statuses:
        print(f"Error: invalid status '{new_status}'. Must be one of {valid_statuses}.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
                   UPDATE movies
                   SET status = ?
                   WHERE id = ?
                   """, (new_status, movie_id))

    connection.commit()
    connection.close()

    print("Movie status updated successfully!")


def get_movies_by_status(status):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
                   SELECT id, tmdb_id, title, release_date, runtime, rating, status
                   FROM movies
                   WHERE status = ?
                   """, (status,))

    movies = cursor.fetchall()

    connection.close()

    return movies