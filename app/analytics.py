from movie_service import get_movies, get_movies_by_status


def average_rating(movies=None):
    if movies is None:
        movies = get_movies()

    ratings = [movie[5] for movie in movies if movie[5] is not None]

    if not ratings:
        return None

    return round(sum(ratings) / len(ratings), 2)


def watched_stats():
    watched = get_movies_by_status("watched")

    return {
        "count": len(watched),
        "average_rating": average_rating(watched)
    }


def top_rated(movies=None, limit=5):
    if movies is None:
        movies = get_movies()

    rated_movies = [movie for movie in movies if movie[5] is not None]
    sorted_movies = sorted(rated_movies, key=lambda m: m[5], reverse=True)

    return sorted_movies[:limit]