"""
Configuration for the Healthsome Flask Application

This module loads environment variables and provides a configuration class
for the application settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class for Flask application."""

    # Secret key for secure Flask sessions
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")

    # Path to the SQLite database file
    DATABASE_FILE = os.getenv("DB_FILE", "healthsome.db")

    # Path to the SQL schema file
    SCHEMA_FILE = os.getenv("SCHEMA_FILE", "schema.sql")

    # Flask-Session configuration
    SESSION_TYPE = "filesystem"  # Store session data in files
    SESSION_PERMANENT = False  # Sessions will not persist beyond browser close

    # Directory to store session files
    SESSION_FILE_DIR = os.getenv("SESSION_FILE_DIR", "./flask_sessions")
