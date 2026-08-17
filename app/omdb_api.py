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
    if not title or not title.strip():
        print("Error: movie title cannot be empty.")
        return None

    params = {
        "apikey": API_KEY,
        "t": title
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("Error: request to OMDb timed out.")
        return None
    except requests.exceptions.ConnectionError:
        print("Error: could not connect to OMDb. Check your internet connection.")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"Error: OMDb returned an HTTP error ({e}).")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: unexpected request failure ({e}).")
        return None

    try:
        data = response.json()
    except ValueError:
        print("Error: OMDb returned an invalid response.")
        return None

    if data.get("Response") == "False":
        print(f"Movie not found: {data.get('Error', 'unknown reason')}")
        return None

    return {
        "imdb_id": data.get("imdbID"),
        "title": data.get("Title"),
        "release_date": parse_release_date(data.get("Released")),
        "runtime": parse_runtime(data.get("Runtime")),
        "rating": float(data.get("imdbRating")) if data.get("imdbRating") not in (None, "N/A") else None,
        "overview": data.get("Plot")
    }