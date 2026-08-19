from handlers import (
    search_movie_handler,
    view_watchlist_handler,
    add_movie_handler,
    change_status_handler,
    rate_movie_handler,
    recommend_movie_handler,
    view_statistics_handler
)
from database import create_tables
import sys

def exit_program():
    print("Goodbye!")
    sys.exit(0)

def main():
    create_tables()

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