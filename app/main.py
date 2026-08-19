from handlers import (
    search_movie_handler,
    view_watchlist_handler,
    add_movie_handler,
    change_status_handler,
    rate_movie_handler,
    recommend_movie_handler,
    view_statistics_handler
)
import sys

def get_valid_status(prompt):
    valid = ("want_to_watch", "watching", "watched")
    while True:
        status = input(prompt).strip()
        if status in valid:
            return status
        print(f"Invalid status. Choose from {valid}.")

def get_valid_rating(prompt):
    while True:
        try:
            rating = float(input(prompt))
            if 0 <= rating <= 10:
                return rating
            print("Rating must be between 0 and 10.")
        except ValueError:
            print("Invalid input. Enter a number.")

def select_movie_by_title(prompt):
    title = input(prompt).strip()
    if not title:
        print("Title cannot be empty.")
        return None
    exact = get_movie_by_exact_title(title)
    if exact:
        return exact
    results = find_movies_by_title(title)
    if not results:
        print(f"No movie found with title containing '{title}'.")
        return None
    if len(results) == 1:
        return results[0]
    print(f"Multiple movies found with '{title}':")
    for idx, movie in enumerate(results, 1):
        print(f"{idx}. {movie[1]} (IMDb: {movie[2]})")
    while True:
        try:
            choice = int(input("Choose a number: "))
            if 1 <= choice <= len(results):
                return results[choice - 1]
            print(f"Please choose between 1 and {len(results)}.")
        except ValueError:
            print("Invalid input. Enter a number.")

def search_movie_handler():
    title = input("Enter movie title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    result = search_movie(title)
    if result:
        print(result)

def view_watchlist_handler():
    status = get_valid_status("Enter status (want_to_watch, watching, watched): ")
    movies = get_movies_by_status(status)
    if not movies:
        print(f"No movies with status '{status}'.")
        return
    for movie in movies:
        print(f"Title: {movie[2]}, Rating: {movie[5]}, Status: {movie[6]}")

def add_movie_handler():
    title = input("Enter movie title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    existing = get_movie_by_exact_title(title)
    if existing:
        print(f"Movie '{existing[1]}' already exists in database.")
        confirm = input("Do you want to add it to your watchlist? (y/n): ").lower()
        if confirm == 'y':
            update_movie_status(existing[0], "want_to_watch")
            print("Movie added to watchlist with status 'want_to_watch'.")
        else:
            print("Operation cancelled.")
        return
    data = search_movie(title)
    if not data:
        return
    add_movie(data["imdb_id"], data["title"], data["release_date"], data["runtime"], data["rating"], data["overview"])
    movie = get_movie_by_title(data["title"])
    if movie:
        update_movie_status(movie[0], "want_to_watch")
        print("Movie added to watchlist with status 'want_to_watch'.")

def change_status_handler():
    movie = select_movie_by_title("Enter movie title: ")
    if not movie:
        return
    print(f"Selected movie: {movie[1]}")
    status = get_valid_status("Enter new status (want_to_watch, watching, watched): ")
    update_movie_status(movie[0], status)

def rate_movie_handler():
    movie = select_movie_by_title("Enter movie title: ")
    if not movie:
        return
    print(f"Selected movie: {movie[1]}")
    rating = get_valid_rating("Enter your rating (0-10): ")
    update_movie_rating(movie[0], rating)

def recommend_movie_handler():
    rec = recommend_movie()
    if rec:
        print(f"Recommended: {rec[2]} (IMDB rating: {rec[5]})")
    else:
        print("No rated movies in your watchlist.")

def view_statistics_handler():
    stats = watched_stats()
    print(f"Watched movies: {stats['count']}, Average rating: {stats['average_rating']}")
    top = top_rated(limit=5)
    if top:
        print("Top rated movies:")
        for movie in top:
            print(f"  {movie[2]} - {movie[5]}")
    else:
        print("No rated movies available.")

def exit_program():
    print("Goodbye!")
    sys.exit(0)

def main():
    menu_actions = {
        1: search_movie_handler,
        2: view_watchlist_handler,
        3: add_movie_handler,
        4: change_status_handler,
        5: rate_movie_handler,
        6: recommend_movie_handler,
        7: view_statistics_handler,
        8: exit_program
    }

    while True:
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
        try:
            choice = int(input("Choose an option : "))
            if choice in menu_actions:
                menu_actions[choice]()
                if choice == 8:
                    break
            else:
                print("Please choose a number between 1 and 8.")
        except ValueError:
            print("Invalid input! Please enter a number.")

if __name__ == "__main__":
    main()