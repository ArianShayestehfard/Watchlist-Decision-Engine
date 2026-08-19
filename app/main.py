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