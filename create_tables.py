import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

from model.groceries import GroceryReceipt, Purchase, Store, User


def setup_database():
    """Create database tables based on SQLModel definitions"""
    # Load environment variables
    load_dotenv(".env.local")

    # Get database connection string from environment or use default
    db_url = os.getenv("DB_URL")

    # Create the database engine
    engine = create_engine(db_url, echo=True)
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Tables created successfully!")


if __name__ == "__main__":
    # Create all tables
    setup_database(models=[User, Store, GroceryReceipt, Purchase])
