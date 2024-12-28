"""
Populate Database Script

This script populates the Healthsome database with demo data for testing purposes.
"""

import os
import random
import sqlite3
from datetime import datetime, timedelta

from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

# Load environment variables from .env file
load_dotenv()

# Retrieve settings from .env file
DB_FILE = os.getenv("DB_FILE", "healthsome.db")
USERNAME = os.getenv("USERNAME", "user")
PASSWORD = os.getenv("PASSWORD", "pass")

def generate_value(min_val, max_val, decimals=1):
    """
    Generate a random value within a range.

    Args:
        min_val (float): Minimum value.
        max_val (float): Maximum value.
        decimals (int): Number of decimal places.

    Returns:
        float: Random value rounded to the specified decimals.
    """
    return round(random.uniform(min_val, max_val), int(decimals))

def insert_user(cursor):
    """
    Insert user data into the database with a hashed password.

    Args:
        cursor (sqlite3.Cursor): Database cursor.

    Returns:
        int: User ID of the created user.
    """
    hashed_password = generate_password_hash(PASSWORD)
    cursor.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (USERNAME, hashed_password)
    )
    user_id = cursor.lastrowid
    print(f"User {USERNAME} created with ID {user_id}.")
    return user_id

def insert_weight(cursor, user_id, start_date):
    """
    Insert weight data for a user into the database.

    Args:
        cursor (sqlite3.Cursor): Database cursor.
        user_id (int): User ID.
        start_date (datetime): Starting date for records.
    """
    print("Adding weight records...")
    for i in range(60):
        date_time = start_date + timedelta(days=i)
        weight_value = generate_value(80, 85, 1)
        date_time_str = date_time.replace(hour=7, minute=0).strftime("%Y-%m-%d %H:%M")
        cursor.execute(
            "INSERT INTO weight (user_id, date_time, weight_value) VALUES (?, ?, ?)",
            (user_id, date_time_str, weight_value)
        )

def insert_bp_pulse(cursor, user_id, start_date):
    """
    Insert blood pressure and pulse data for a user into the database.

    Args:
        cursor (sqlite3.Cursor): Database cursor.
        user_id (int): User ID.
        start_date (datetime): Starting date for records.
    """
    print("Adding blood pressure and pulse records...")
    for i in range(60):
        for hour in [7, 19]:  # Morning and evening
            date_time = start_date + timedelta(days=i, hours=hour)
            systolic = generate_value(110, 140, 0)
            diastolic = generate_value(70, 90, 0)
            pulse = generate_value(60, 100, 0)
            date_time_str = date_time.strftime("%Y-%m-%d %H:%M")
            cursor.execute(
                "INSERT INTO blood_pressure (user_id, date_time, systolic, diastolic, pulse) "
                "VALUES (?, ?, ?, ?, ?)",
                (user_id, date_time_str, systolic, diastolic, pulse)
            )

def insert_medications(cursor, user_id, start_date):
    """
    Insert medication records for a user into the database.

    Args:
        cursor (sqlite3.Cursor): Database cursor.
        user_id (int): User ID.
        start_date (datetime): Starting date for records.
    """
    print("Adding medication records...")
    medications = [
        ("Morning Med", "1 tablet"),
        ("Afternoon Med", "1/2 tablet"),
        ("Evening Med", "2 tablets")
    ]
    for i in range(60):
        date_time = start_date + timedelta(days=i)
        for hour, (medication_name, dosage) in zip([7, 13, 20], medications):
            taken = 0 if random.random() < 0.1 else 1  # 10% chance of missing the medication
            date_time_str = date_time.replace(hour=hour, minute=0).strftime("%Y-%m-%d %H:%M")
            cursor.execute(
                "INSERT INTO medications (user_id, date_time, medication_name, dosage, taken) "
                "VALUES (?, ?, ?, ?, ?)",
                (user_id, date_time_str, medication_name, dosage, taken)
            )

def populate_database():
    """
    Populate the database with demo data.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    start_date = datetime.now() - timedelta(days=60)

    try:
        user_id = insert_user(cursor)
        insert_weight(cursor, user_id, start_date)
        insert_bp_pulse(cursor, user_id, start_date)
        insert_medications(cursor, user_id, start_date)
        conn.commit()
        print("Database populated successfully.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    populate_database()
