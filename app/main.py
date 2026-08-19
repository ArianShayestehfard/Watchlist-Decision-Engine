from recommendation import recommend_movie, recommend_top_n

best = recommend_movie()
print(f"Recommended: {best}")

print("--- Top 3 recommendations ---")
for movie in recommend_top_n(3):
    print(movie)