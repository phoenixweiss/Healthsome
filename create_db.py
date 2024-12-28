"""
Database Initialization Script

This script initializes the SQLite database for the Healthsome application
using the schema specified in the environment variables.
"""

import os
import sqlite3
from app import create_app

def initialize_database():
    """
    Initialize the database using the schema file specified in the .env file.

    Reads the schema from the file and creates the SQLite database.
    """
    schema_file = os.getenv("SCHEMA_FILE", "schema.sql")
    db_file = os.getenv("DB_FILE", "default.db")

    if not os.path.exists(schema_file):
        print(f"Schema file '{schema_file}' not found.")
        return

    # Check if the database file already exists
    if os.path.exists(db_file):
        confirm = input(
            f"Database file '{db_file}' already exists. Recreate? (y/n): "
        ).strip().lower()
        if confirm != 'y':
            print("Initialization aborted.")
            return
        os.remove(db_file)  # Remove the existing database file

    try:
        with sqlite3.connect(db_file) as conn:
            with open(schema_file, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
        print(f"Database initialized successfully using schema from '{schema_file}'.")
    except (sqlite3.DatabaseError, OSError) as e:
        print(f"Error initializing database: {e}")

def main():
    """
    Main function to initialize the database within the Flask app context.
    """
    app = create_app()
    with app.app_context():
        initialize_database()

if __name__ == "__main__":
    main()
