from database import get_connection


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