from movie_service import get_movies_by_status


def recommend_movie():
    candidates = get_movies_by_status("want_to_watch")

    rated_candidates = [movie for movie in candidates if movie[5] is not None]

    if not rated_candidates:
        return None

    return max(rated_candidates, key=lambda m: m[5])

