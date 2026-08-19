from recommender import MovieRecommender

_recommender = None

def get_recommender():
    global _recommender
    if _recommender is None:
        _recommender = MovieRecommender()
    return _recommender

def recommend_movie():
    candidates = get_movies_by_status("want_to_watch")
    rated_candidates = [movie for movie in candidates if movie[5] is not None]
    if not rated_candidates:
        return None
    return max(rated_candidates, key=lambda m: m[5])

def recommend_top_n(n=3):
    candidates = get_movies_by_status("want_to_watch")
    rated_candidates = [movie for movie in candidates if movie[5] is not None]
    sorted_candidates = sorted(rated_candidates, key=lambda m: m[5], reverse=True)
    return sorted_candidates[:n]