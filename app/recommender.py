import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from movie_service import get_movies, get_movie_by_id
from database import get_connection

class MovieRecommender:
    def __init__(self):
        self.movies_df = None
        self.tfidf_matrix = None
        self.cosine_sim = None
        self._last_movie_count = 0
        self.fit()

    def fit(self):
        movies = get_movies()
        if not movies:
            self.movies_df = pd.DataFrame()
            return
        df = pd.DataFrame(movies, columns=['id', 'imdb_id', 'title', 'release_date', 'runtime', 'rating'])
        df['overview'] = df['id'].apply(self._get_overview)
        df['genres'] = df['id'].apply(self._get_genres)
        df['combined_features'] = df['overview'].fillna('') + ' ' + df['genres'].fillna('')
        self.movies_df = df
        self._last_movie_count = len(movies)
        tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = tfidf.fit_transform(df['combined_features'])
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def _get_overview(self, movie_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT overview FROM movies WHERE id = ?", (movie_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else ""

    def _get_genres(self, movie_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT g.name FROM genres g
                                              JOIN movie_genres mg ON g.id = mg.genre_id
                       WHERE mg.movie_id = ?
                       """, (movie_id,))
        genres = cursor.fetchall()
        conn.close()
        return ' '.join([g[0] for g in genres])

    def _needs_update(self):
        current_count = len(get_movies())
        return current_count != self._last_movie_count

    def get_user_profile(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT movie_id, user_rating FROM ratings")
        ratings = cursor.fetchall()
        conn.close()
        if not ratings:
            return None
        df = pd.DataFrame(ratings, columns=['movie_id', 'user_rating'])
        return df.groupby('movie_id')['user_rating'].mean()

    def recommend_for_user(self, top_n=5):
        if self._needs_update():
            self.fit()
        user_profile = self.get_user_profile()
        if user_profile is None or self.movies_df.empty:
            return []

        watched_movies = set()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT movie_id FROM watchlist WHERE status = 'watched'")
        for row in cursor.fetchall():
            watched_movies.add(row[0])
        conn.close()

        rated_movies = set(user_profile.index)
        similarity_scores = {}

        for movie_id, avg_rating in user_profile.items():
            idx = self.movies_df[self.movies_df['id'] == movie_id].index
            if len(idx) == 0:
                continue
            idx = idx[0]
            sim_scores = list(enumerate(self.cosine_sim[idx]))
            for i, score in sim_scores:
                movie = self.movies_df.iloc[i]
                if movie['id'] not in watched_movies and movie['id'] not in rated_movies:
                    if movie['id'] not in similarity_scores:
                        similarity_scores[movie['id']] = 0
                    similarity_scores[movie['id']] += score * avg_rating

        for movie_id in rated_movies:
            if movie_id in similarity_scores:
                del similarity_scores[movie_id]

        sorted_movies = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for movie_id, score in sorted_movies[:top_n]:
            movie = get_movie_by_id(int(movie_id))
            if movie:
                results.append((movie[0], movie[1], round(score, 2)))
        return results