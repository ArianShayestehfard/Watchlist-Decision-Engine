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
    while choice != 8:
      if choice == 1:
        print("Search Movie")
      elif choice == 2:
        print("View Watchlist")
      elif choice == 3:
        print("Add Movie to Watchlist")
      elif choice == 4:
        print("Change Movie Status")
      elif choice == 5:
        print("Rate Movie")
      elif choice == 6:
        print("Recommend Movie")
      elif choice == 7:
        print("View Statistics")
      elif choice == 8:
        print("Goodbye!")
      else:
        print("Please choose a number between 1 and 8.")
except ValueError:
    print("Invalid input! Please enter a number.")

