import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine


def setup_database():
    """Create database tables based on SQLModel definitions"""
    # Load environment variables
    load_dotenv(".env.local")

    # Get database connection string from environment or use default
    db_url = os.getenv("DATABASE_URL")

    # Create the database engine
    engine = create_engine(db_url, echo=True)
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Tables created successfully!")


if __name__ == "__main__":
    # Create all tables
    setup_database()
