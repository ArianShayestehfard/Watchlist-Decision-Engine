import os
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")


def search_movie(title):
    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key": API_KEY,
        "query": title
    }

    response = requests.get(url, params=params)

    return response.json()