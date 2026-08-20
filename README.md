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

A typical workflow is:

```text
Search Movie
     │
     ▼
Add to Watchlist
     │
     ▼
Watch / Rate Movies
     │
     ▼
Build Personal Preference Signal
     │
     ▼
Recommendation Engine
     │
     ▼
🎯 Recommended Movies
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

---

### 📋 Watchlist Management

Movies can be tracked using three states:

```text
want_to_watch
watching
watched
```

This allows the application to distinguish between planned, currently watched, and completed movies.

---

### ⭐ Personal Ratings

The system stores the user's own rating separately from IMDb's public rating.

```text
IMDb Rating      → External movie rating
Personal Rating  → User preference signal
```

Personal ratings are then used by the recommendation engine.

---

### 🎯 Personalized Recommendations

The system uses a **content-based filtering approach** based on:

* Movie genres
* Plot descriptions
* Personal ratings

The recommendation pipeline is:

```text
Movie Metadata
      │
      ▼
Genres + Plot
      │
      ▼
TF-IDF Vectorization
      │
      ▼
Cosine Similarity
      │
      ▼
Personal Rating Weight
      │
      ▼
Candidate Filtering
      │
      ▼
Ranked Recommendations
```

---

### 📊 Watchlist Analytics

The application provides statistics including:

* Average rating of watched movies
* Top-rated movies
* Watchlist information

---

### 🌱 Batch Movie Import

A curated list of popular movies can be imported into the database to quickly create a useful dataset for testing and experimentation.

---

### 🛡️ Input Validation & Error Handling

The application includes validation and error handling for situations such as:

* Invalid user input
* Invalid ratings
* Invalid watchlist status
* Missing movie information
* API/network failures
* Missing configuration

---

# 🤖 Recommendation Engine

## How does it work?

The recommendation engine uses **TF-IDF** and **cosine similarity** to compare movies based on their textual characteristics.

### 1. Feature Construction

For each movie, genres and plot information are combined into a textual representation.

```text
Genres + Plot Overview
          │
          ▼
     Movie Features
```

### 2. TF-IDF

`TfidfVectorizer` converts the movie text into numerical vectors.

```text
Movie Text
    │
    ▼
TF-IDF Vectorization
    │
    ▼
Numerical Feature Vectors
```

### 3. Similarity

`cosine_similarity` calculates how similar movies are to one another.

```text
Movie A ───────────── Movie B
          │
          ▼
   Cosine Similarity
```

### 4. Personalization

The similarity scores are influenced by the user's own movie ratings.

Conceptually:

```text
Similarity × Personal Rating
            │
            ▼
 Recommendation Contribution
```

Highly-rated movies therefore have a stronger influence on the final ranking.

### 5. Filtering

Movies that have already been rated or marked as watched are excluded from the recommendation candidates.

### 6. Ranking

The remaining candidates are ranked by their accumulated recommendation score.

```text
              Candidate Movies
                      │
                      ▼
              Similarity Scores
                      │
                      ▼
              Rating Influence
                      │
                      ▼
                  Filtering
                      │
                      ▼
                   Ranking
                      │
                      ▼
             🎯 Top Recommendations
```

This makes the current system a **content-based recommendation system**, rather than a collaborative filtering system.

---

# 🧠 Why a Decision Support System?

A traditional watchlist application mainly performs CRUD operations:

```text
Create
Read
Update
Delete
```

This project adds a decision-making layer.

```text
              Movie Data
                  │
                  ▼
          User Interaction
                  │
                  ▼
          Personal Ratings
                  │
                  ▼
        Similarity Analysis
                  │
                  ▼
               Ranking
                  │
                  ▼
          Recommendation
                  │
                  ▼
          Decision Support
```

The goal is not only to **store information**, but to transform stored information into an actionable recommendation.

---

# 🏗️ Architecture

```text
                         ┌─────────────────┐
                         │    User / CLI   │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     main.py     │
                         │   CLI / Menu    │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   handlers.py   │
                         └────────┬────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
       ┌────────────┐      ┌──────────────┐   ┌───────────────┐
       │ validators │      │movie_service │   │recommendation │
       └────────────┘      └───────┬──────┘   └───────┬───────┘
                                   │                   │
                                   ▼                   ▼
                           ┌──────────────┐    ┌──────────────┐
                           │  database.py │    │ recommender  │
                           └───────┬──────┘    │ TF-IDF +     │
                                   │           │ cosine       │
                                   ▼           │ similarity   │
                           ┌──────────────┐    └──────────────┘
                           │    SQLite    │
                           │   Database   │
                           └──────────────┘

                           ┌──────────────┐
                           │   OMDb API   │
                           └──────┬───────┘
                                  │
                                  ▼
                           ┌──────────────┐
                           │ omdb_api.py  │
                           └──────────────┘
```

---

# 🗄️ Database Design

The application uses SQLite with separate tables for movie metadata, genres, personal ratings, and watchlist state.

```text
                  ┌───────────────┐
                  │    movies     │
                  └───────┬───────┘
                          │
             ┌────────────┼────────────┐
             │            │            │
             ▼            ▼            ▼
       ┌──────────┐ ┌───────────┐ ┌────────────┐
       │ ratings  │ │ watchlist │ │movie_genres│
       └──────────┘ └───────────┘ └──────┬─────┘
                                         │
                                         ▼
                                   ┌───────────┐
                                   │  genres   │
                                   └───────────┘
```

### Main tables

| Table          | Purpose                                 |
| -------------- | --------------------------------------- |
| `movies`       | Core movie metadata                     |
| `genres`       | Normalized genre information            |
| `movie_genres` | Movie ↔ genre many-to-many relationship |
| `ratings`      | User's personal ratings                 |
| `watchlist`    | Movie watch status                      |

The user's personal rating is deliberately kept separate from IMDb's public rating.

---

# 🛠️ Technology Stack

| Technology        | Purpose                        |
| ----------------- | ------------------------------ |
| **Python 3.11+**  | Application and business logic |
| **SQLite**        | Relational data storage        |
| **OMDb API**      | Movie metadata                 |
| **Pandas**        | Data processing                |
| **Scikit-learn**  | TF-IDF and cosine similarity   |
| **Requests**      | HTTP communication             |
| **python-dotenv** | Environment configuration      |
| **Pytest**        | Automated testing              |

---

# 🚀 Quick Start

## Prerequisites

* Python 3.11+
* A free OMDb API key

Get an API key from:

https://www.omdbapi.com/apikey.aspx

## Clone the repository

```bash
git clone https://github.com/ArianShayestehfard/Watchlist-Decision-Engine.git
cd Watchlist-Decision-Engine
```

## Create a virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Configure OMDb

Create a `.env` file based on `.env.example`:

```env
OMDB_API_KEY=your_actual_key_here
```

> ⚠️ Never commit your real API key to GitHub.

## Run the application

```bash
cd app
python main.py
```

The SQLite database is created automatically when required.

---

# 🧪 Testing

Run the automated tests from the project root:

```bash
pytest tests/ -v
```

The test suite covers important application behavior including:

* OMDb response parsing
* Runtime parsing
* Release-date parsing
* Analytics calculations
* Recommendation-related regression cases

---

# 📁 Project Structure

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
├── database/
│
├── docs/
│
├── .github/
│   └── workflows/
│
├── .env.example
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── README.md
└── requirements.txt
```

---

# 📌 Current Limitations

The current implementation intentionally focuses on a lightweight, interpretable recommendation model.

* Recommendations are based on genres and plot text.
* Actors and directors are not currently used as recommendation features.
* The system does not currently implement collaborative filtering.
* At least one personal rating is needed to build a recommendation signal.
* The application is currently designed around a local/single-user workflow.
* OMDb API availability and request limits can affect movie retrieval.

---

# 🗺️ Roadmap

## Recommendation

* [ ] Recommendation explanations
* [ ] Genre preference weighting
* [ ] Runtime preference
* [ ] Release-year preference
* [ ] Recommendation score breakdown
* [ ] Semantic embeddings
* [ ] Collaborative filtering

## Engineering

* [ ] Expand automated test coverage
* [ ] GitHub Actions CI
* [ ] Improve application architecture
* [ ] Add database migrations
* [ ] Improve error reporting

## Product

* [ ] FastAPI backend
* [ ] PostgreSQL support
* [ ] Web interface
* [ ] Multi-user support
* [ ] Docker deployment

---

# 📚 Documentation

Technical documentation:

* [Architecture](docs/architecture.md)
* [Database Design](docs/database.md)
* [Recommendation Engine](docs/recommendation.md)

---

# 👨‍💻 Author

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

# 📄 License

This project is licensed under the **MIT License**.

See [LICENSE](LICENSE) for details.

---

<p align="center">
  Built with Python, SQLite, Pandas, and Scikit-learn.
</p>
