from analytics import average_rating, top_rated

SAMPLE_MOVIES = [
    (1, "tt0001", "Movie A", "2020-01-01", 120, 8.5),
    (2, "tt0002", "Movie B", "2021-01-01", 100, 9.0),
    (3, "tt0003", "Movie C", "2022-01-01", 90, None),
]


def test_average_rating_ignores_missing_values():
    assert average_rating(SAMPLE_MOVIES) == 8.75


def test_average_rating_empty_list():
    assert average_rating([]) is None


def test_top_rated_orders_by_rating_descending():
    result = top_rated(SAMPLE_MOVIES, limit=2)
    titles = [movie[2] for movie in result]
    assert titles == ["Movie B", "Movie A"]


def test_top_rated_excludes_unrated_movies():
    result = top_rated(SAMPLE_MOVIES, limit=10)
    assert all(movie[5] is not None for movie in result)
