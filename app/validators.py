from constants import VALID_STATUSES
from movie_service import find_movies_by_title, get_movie_by_exact_title

def get_valid_status(prompt):
    while True:
        status = input(prompt).strip()
        if status in VALID_STATUSES:
            return status
        print(f"Invalid status. Choose from {VALID_STATUSES}.")

