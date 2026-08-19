from movie_service import import_500_movies
from database import create_tables

if __name__ == "__main__":
    print("Creating database tables")
    create_tables()

    print("Seeding database with movies")
    import_500_movies(delay=0.5)

    print("✅ Database is ready!")