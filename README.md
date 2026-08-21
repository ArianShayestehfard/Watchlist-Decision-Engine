<h1 align="center">🎬 Watchlist Decision Engine</h1>

<p align="center">
  Personalized movie recommendation and decision-support system built with Python, SQLite, OMDb API, Pandas, and Scikit-learn.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/API-OMDb-FF6F00" alt="OMDb API">
  <img src="https://img.shields.io/badge/ML-Scikit--learn-F7931E?logo=scikit-learn&logoColor=white" alt="Scikit-learn">
  <img src="https://img.shields.io/badge/Data-Pandas-150458?logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/Testing-Pytest-0A9EDC?logo=pytest&logoColor=white" alt="Pytest">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
</p>

---

## 🎯 Overview

**Watchlist Decision Engine** is a command-line movie recommendation and decision-support system that goes beyond a traditional watchlist.

Instead of simply storing movies, the system uses the user's **personal ratings, movie genres, and plot descriptions** to determine which unseen movies are most similar to the movies the user enjoyed.

The project combines:

* 🎬 Real movie metadata from the OMDb API
* 🗄️ Relational database design with SQLite
* ⭐ Personal movie ratings
* 📋 Watchlist state management
* 🤖 Content-based recommendation
* 📊 Basic watchlist analytics
* 🧪 Automated testing

The core idea is simple:

> **Turn a movie watchlist into a system that can help decide what to watch next.**

---

## 🎮 Application

The application runs as an interactive command-line system:

```text
╔══════════════════════════════════════════╗
║       🎬 AI MOVIE RECOMMENDATION         ║
╚══════════════════════════════════════════╝

1- 🔎 Search Movie
2- 📋 View Watchlist
3- ➕ Add Movie to Watchlist
4- 🔄 Change Movie Status
5- ⭐ Rate Movie
6- 🎯 Recommend Movie
7- 📊 View Statistics
8- 🚪 Exit
```

---

## ✨ Features

### 🔎 Movie Search

Search for movies by title through the **OMDb API** and retrieve information such as:

* Title
* Release year
* Runtime
* Genres
* Plot overview
* IMDb rating

### 📋 Watchlist Management

Movies can be tracked using three states: `want_to_watch`, `watching`, `watched`. This allows the application to distinguish between planned, currently watched, and completed movies.

### ⭐ Personal Ratings

The system stores the user's own rating separately from IMDb's public rating. IMDb's rating is external reference data; the personal rating is the actual preference signal the recommendation engine learns from.

### 🎯 Personalized Recommendations

The system uses a **content-based filtering approach** based on movie genres, plot descriptions, and personal ratings.

### 📊 Watchlist Analytics

The application provides statistics including average rating of watched movies and top-rated movies in the list.

### 🌱 Batch Movie Import

A curated list of popular movies can be imported into the database to quickly create a useful dataset for testing and experimentation.

### 🛡️ Input Validation & Error Handling

The application validates user input (status, rating, movie selection) and handles OMDb network failures, timeouts, and missing configuration without crashing.

---

## 🤖 Recommendation Engine

The recommendation engine uses **TF-IDF** and **cosine similarity** to compare movies based on their textual characteristics.

```text
Genres + Plot Overview
          │
          ▼
   TF-IDF Vectorization
          │
          ▼
    Cosine Similarity
          │
          ▼
  Weighted by Personal Rating
          │
          ▼
Filter out rated / watched movies
          │
          ▼
   🎯 Ranked Recommendations
```

1. Each movie's genres and plot are combined into a single text feature.
2. `TfidfVectorizer` converts that text into numerical vectors; `cosine_similarity` compares every movie against every other movie.
3. For each movie the user personally rated, similar movies are found and weighted by how highly the user rated the original.
4. Movies already rated or marked `watched` are excluded from the results.
5. The remaining candidates are ranked by accumulated score.

This makes it a **content-based recommendation system**, not collaborative filtering — recommendations only start appearing once you've rated at least one movie.

---

## 🏗️ Architecture

```text
User / CLI
    │
    ▼
main.py (menu loop)
    │
    ▼
handlers.py
    │
    ├──▶ validators.py
    ├──▶ movie_service.py ──▶ database.py ──▶ SQLite
    └──▶ recommendation.py ──▶ recommender.py (TF-IDF + cosine similarity)

omdb_api.py ──▶ OMDb API
```

---

## 🗄️ Database Design

| Table          | Purpose                                 |
| -------------- | ---------------------------------------- |
| `movies`       | Core movie metadata cached from OMDb     |
| `genres`       | Normalized genre lookup table            |
| `movie_genres` | Movie ↔ genre many-to-many relationship |
| `ratings`      | User's personal ratings                  |
| `watchlist`    | Movie watch status                       |

The user's personal rating is deliberately kept separate from IMDb's public rating.

---

## 🛠️ Technology Stack

| Technology        | Purpose                        |
| ------------------ | ------------------------------- |
| **Python 3.11+**  | Application and business logic |
| **SQLite**         | Relational data storage        |
| **OMDb API**       | Movie metadata                 |
| **Pandas**         | Data processing                |
| **Scikit-learn**  | TF-IDF and cosine similarity   |
| **Requests**       | HTTP communication             |
| **python-dotenv** | Environment configuration      |
| **Pytest**         | Automated testing               |

---

## 🚀 Quick Start

### Prerequisites

* Python 3.11+
* A free OMDb API key from [omdbapi.com/apikey.aspx](https://www.omdbapi.com/apikey.aspx)

### Setup

```bash
git clone https://github.com/ArianShayestehfard/Watchlist-Decision-Engine.git
cd Watchlist-Decision-Engine

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file inside `app/` based on `.env.example`:

```env
OMDB_API_KEY=your_actual_key_here
```

> ⚠️ Never commit your real API key to GitHub.

### Run

```bash
cd app
python main.py
```

The SQLite database is created automatically on first run.

### (Optional) Seed the database

```bash
python seed_data.py
```

---

## 🧪 Testing

```bash
pytest tests/ -v
```

The test suite covers OMDb response parsing (release date, runtime), analytics calculations, and a regression test for a real bug found during development (a `numpy.int64` type mismatch that silently broke database lookups in the recommender).

---

## 📁 Project Structure

```text
Watchlist-Decision-Engine/
│
├── app/
│   ├── main.py
│   ├── handlers.py
│   ├── validators.py
│   ├── constants.py
│   ├── database.py
│   ├── movie_service.py
│   ├── omdb_api.py
│   ├── movie_list.py
│   ├── recommendation.py
│   ├── recommender.py
│   ├── analytics.py
│   └── seed_data.py
│
├── tests/
│   ├── conftest.py
│   ├── test_omdb_api.py
│   ├── test_analytics.py
│   └── test_recommender_types.py
│
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## 📌 Current Limitations

* Recommendations are based on genres and plot text only — actors and directors are not currently used as features.
* No collaborative filtering; this is a single-user, content-based system.
* At least one personal rating is needed before any recommendation can be generated.
* Designed around a local, single-user workflow.
* OMDb API availability and rate limits can affect movie retrieval.

---

## 🗺️ Roadmap

**Recommendation**
- [ ] Recommendation explanations (why a movie was suggested)
- [ ] Genre / runtime / release-year preference weighting
- [ ] Collaborative filtering

**Engineering**
- [ ] Expand automated test coverage
- [ ] GitHub Actions CI
- [ ] Database migrations

**Product**
- [ ] Web interface (FastAPI backend)
- [ ] Multi-user support

---

## 👨‍💻 Author

<p align="center">
  <b>Arian Shayestehfard</b>
  <br>
  Computer Engineering Student
  <br><br>
  <a href="https://github.com/ArianShayestehfard">
    <img src="https://img.shields.io/badge/GitHub-ArianShayestehfard-181717?logo=github&logoColor=white" alt="GitHub">
  </a>
</p>

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

<p align="center">
  Built with Python, SQLite, Pandas, and Scikit-learn.
</p>
