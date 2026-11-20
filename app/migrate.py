"""Create the tables in the database. Safe to run again and again.

Run:  python -m app.migrate
CD runs this on Neon BEFORE deploying, so the database is ready for the new version.
"""
from app.db import Base, get_engine


def main() -> None:
    Base.metadata.create_all(get_engine())
    print("Database is ready: table 'notes' exists")


if __name__ == "__main__":
    main()
