# Watchlist Decision Engine

A command-line movie watchlist manager with a content-based recommendation engine, built in Python with SQLite and the OMDb API.

Unlike a simple watchlist CRUD app, this project tries to actually help decide **what to watch next**. It fetches real movie data from an external API, stores it in a relational database, tracks personal ratings and watch status, and uses TF-IDF + cosine similarity over movie genres and plot summaries to recommend titles similar to the ones you've rated highly.

## Features

- **Search** any movie by title via the OMDb API (title, year, runtime, genres, plot, IMDb rating)
- **Watchlist management** with three states: `want_to_watch`, `watching`, `watched`
- **Personal ratings** (separate from IMDb's public rating) that feed the recommender
- **Content-based recommendation engine** using TF-IDF vectorization and cosine similarity over genres + plot overview
- **Analytics**: average rating of watched movies, top-rated movies in your list
- **Batch import** of a curated list of popular movies for quickly seeding the database
- Input validation and error handling for network failures, invalid input, and missing data

## Tech Stack

- **Python 3.11+**
- **SQLite** — relational storage for movies, genres, ratings, and watchlist status
- **OMDb API** — external source of movie metadata
- **pandas** — tabular data handling for the recommender
- **scikit-learn** — `TfidfVectorizer` and `cosine_similarity` for content-based filtering
- **python-dotenv** — environment variable management
- **pytest** — unit and regression testing

## Architecture

```
User (CLI)
   │
   ▼
main.py ──────────► handlers.py ──────────► validators.py
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
     omdb_api.py    movie_service.py  recommendation.py
          │               │                 │
          ▼               ▼                 ▼
     OMDb API          database.py     recommender.py
      (HTTP)               │          (TF-IDF + cosine
                            ▼           similarity)
                        SQLite
                     (watchlist.db)
```

The database has four tables: `movies` (core metadata), `genres` and `movie_genres` (many-to-many), `ratings` (personal user ratings, separate from IMDb's public rating), and `watchlist` (status tracking per movie).

## Getting Started

### Prerequisites

- Python 3.11 or later
- A free [OMDb API key](https://www.omdbapi.com/apikey.aspx)

### Installation

```bash
git clone https://github.com/ArianShayestehfard/Watchlist-Decision-Engine.git
cd Watchlist-Decision-Engine

python -m venv .venv
source .venv/bin/activate      # on Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### Configuration

Copy the example environment file and add your OMDb API key:

```bash
cp .env.example app/.env
```

Then edit `app/.env`:

```
OMDB_API_KEY=your_actual_key_here
```

### Running the app

```bash
cd app
python main.py
```

On first run, the SQLite database and all tables are created automatically at `database/watchlist.db`.

### Running the tests

```bash
pytest tests/
```

## Usage

The app runs as an interactive CLI menu:

```
1. Search Movie
2. View Watchlist
3. Add Movie to Watchlist
4. Change Movie Status
5. Rate Movie
6. Recommend Movie
7. View Statistics
8. Exit
```

A typical flow: search and add a few movies (option 3), rate the ones you've already seen (option 5), then ask for a recommendation (option 6) — the engine finds unrated movies in your list whose genres and plot are most similar to what you rated highly.

## How the Recommendation Engine Works

1. Every movie's genres and plot overview are combined into a single text field.
2. `TfidfVectorizer` converts these text fields into weighted vectors.
3. `cosine_similarity` computes a similarity matrix between every pair of movies.
4. For each movie you've personally rated, the engine finds similar movies and weights the similarity score by your rating.
5. Movies you've already rated or marked as `watched` are excluded from the results.
6. The remaining candidates are ranked by their accumulated similarity score.

This is a form of **content-based filtering** — recommendations come from movie attributes (genre, plot), not from other users' behavior.

## Known Limitations

- Content-based filtering only considers genres and plot text; it has no notion of actors, directors, or user-to-user collaborative signals.
- The recommender needs at least one personally rated movie to produce results.
- OMDb's free tier has a daily request limit.

## Project Structure

```
Watchlist-Decision-Engine/
├── app/
│   ├── main.py              # CLI entry point and menu loop
│   ├── handlers.py          # Menu action handlers
│   ├── validators.py        # User input validation
│   ├── constants.py         # Shared constants (statuses, menu labels)
│   ├── database.py          # SQLite connection and schema setup
│   ├── movie_service.py     # Movie/genre/watchlist data access layer
│   ├── omdb_api.py          # OMDb API client and response parsing
│   ├── movie_list.py        # Seed list of popular movies
│   ├── recommendation.py    # Recommendation engine facade
│   ├── recommender.py       # TF-IDF / cosine similarity implementation
│   ├── analytics.py         # Watchlist statistics
│   └── seed_data.py         # Database seeding script
├── tests/
│   ├── conftest.py
│   ├── test_omdb_api.py
│   └── test_recommender_regression.py
├── requirements.txt
├── .env.example
├── .gitignore
└── LICENSE
```

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
