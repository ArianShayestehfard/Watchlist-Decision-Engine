def search_movie_handler():
    title = input("Enter movie title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    result = search_movie(title)
    if result:
        print(result)

