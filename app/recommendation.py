from recommender import MovieRecommender

_recommender = None

def get_recommender():
    global _recommender
    if _recommender is None:
        _recommender = MovieRecommender()
    return _recommender

def recommend_movie():
    recommender = get_recommender()
    recommendations = recommender.recommend_for_user(top_n=1)
    return recommendations[0] if recommendations else None

def recommend_top_n(n=3):
    recommender = get_recommender()
    return recommender.recommend_for_user(top_n=n)