from movie_service import add_movie, update_movie_rating, update_movie_status, get_movies_by_status
from recommendation import recommend_movie
from analytics import watched_stats, top_rated
from omdb_api import search_movie
import sys

print("""
🎬 AI MOVIE RECOMMENDATION SYSTEM            
                                          
1- 🔎  Search Movie                                
2- 📋  View Watchlist                             
3- ➕  Add Movie to Watchlist                    
4- 🔄  Change Movie Status                        
5- ⭐  Rate Movie                                 
6- 🎯  Recommend Movie                          
7- 📊  View Statistics                           
8- 🚪  Exit                                       
                                                   
Choose an option please                   
""")

def search_movie_interactive():
    title = input("Enter movie title: ")
    result = search_movie(title)
    if result:
        print(result)
    return None

def view_watchlist_interactive():
    status = input("Enter status (want_to_watch, watching, watched): ")
    movies = get_movies_by_status(status)
    for m in movies:
        print(f"ID: {m[0]}, Title: {m[2]}, Rating: {m[5]}, Status: {m[6]}")
    return None

def add_movie_interactive():
    title = input("Enter movie title: ")
    data = search_movie(title)
    if data:
        add_movie(data["imdb_id"], data["title"], data["release_date"], data["runtime"], data["rating"], data["overview"])
        # دریافت شناسه فیلم تازه اضافه شده
        from movie_service import get_movie_by_title
        movie = get_movie_by_title(data["title"])
        if movie:
            update_movie_status(movie[0], "want_to_watch")
            print("Movie added to watchlist with status 'want_to_watch'.")
    return None

def change_status_interactive():
    movie_id = int(input("Enter movie ID: "))
    status = input("Enter new status (want_to_watch, watching, watched): ")
    update_movie_status(movie_id, status)
    return None

def rate_movie_interactive():
    movie_id = int(input("Enter movie ID: "))
    rating = float(input("Enter your rating (0-10): "))
    update_movie_rating(movie_id, rating)
    return None

def recommend_interactive():
    rec = recommend_movie()
    if rec:
        print(f"Recommended: {rec[2]} (IMDB rating: {rec[5]})")
    else:
        print("No rated movies in your watchlist.")
    return None

def statistics_interactive():
    stats = watched_stats()
    print(f"Watched movies: {stats['count']}, Average rating: {stats['average_rating']}")
    top = top_rated(limit=5)
    print("Top rated movies:")
    for m in top:
        print(f"  {m[2]} - {m[5]}")
    return None

def exit_program():
    print("Goodbye!")
    sys.exit(0)

menu_actions = {
    1: search_movie_interactive,
    2: view_watchlist_interactive,
    3: add_movie_interactive,
    4: change_status_interactive,
    5: rate_movie_interactive,
    6: recommend_interactive,
    7: statistics_interactive,
    8: exit_program
}

while True:

    try:
        choice = int(input("Choose an option : "))

        if choice in menu_actions:
            result = menu_actions[choice]()
            if choice == 8:
                break
        else:
            print("Please choose a number between 1 and 8.")

    except ValueError:
        print("Invalid input! Please enter a number.")