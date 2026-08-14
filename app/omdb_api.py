import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OMDB_API_KEY")
BASE_URL = "http://www.omdbapi.com/"


def parse_release_date(raw_date):
    try:
        return datetime.strptime(raw_date, "%d %b %Y").strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return None


def parse_runtime(raw_runtime):
    try:
        return int(raw_runtime.split(" ")[0])
    except (ValueError, AttributeError):
        return None


def search_movie(title):
    params = {
        "apikey": API_KEY,
        "t": title
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    data = response.json()

    if data.get("Response") == "False":
        return None

    return {
        "imdb_id": data.get("imdbID"),
        "title": data.get("Title"),
        "release_date": parse_release_date(data.get("Released")),
        "runtime": parse_runtime(data.get("Runtime")),
        "rating": float(data.get("imdbRating")) if data.get("imdbRating") not in (None, "N/A") else None,
        "overview": data.get("Plot")
    }