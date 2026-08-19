from constants import VALID_STATUSES
from movie_service import find_movies_by_title, get_movie_by_exact_title

def get_valid_status(prompt):
    while True:
        status = input(prompt).strip()
        if status in VALID_STATUSES:
            return status
        print(f"Invalid status. Choose from {VALID_STATUSES}.")

def get_valid_rating(prompt):
    while True:
        try:
            rating = float(input(prompt))
            if 0 <= rating <= 10:
                return rating
            print("Rating must be between 0 and 10.")
        except ValueError:
            print("Invalid input. Enter a number.")

