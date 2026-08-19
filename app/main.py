from movie_service import add_movies_batch, get_movies

result = add_movies_batch([
    "Interstellar",
    "Inception",
    "The Matrix",
    "Parasite"
])

print(f"Added: {result['added']}")
print(f"Failed: {result['failed']}")

for movie in get_movies():
    print(movie)