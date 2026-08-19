from analytics import watched_stats, top_rated

stats = watched_stats()
print(f"Watched: {stats['count']} movies, average rating: {stats['average_rating']}")

print("--- Top rated in your list ---")
for movie in top_rated(limit=3):
    print(movie)