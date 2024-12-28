"""
Datetime Helpers for the Healthsome application.

This module provides utility functions for handling datetime strings
and calculating date ranges for filtering data.
"""

from datetime import datetime, timedelta

def to_iso_format(dt_str):
    """
    Convert a datetime string from HTML datetime-local format to ISO format.

    Args:
        dt_str (str): The datetime string in HTML datetime-local format (e.g., '2024-12-18T19:25').

    Returns:
        str: The datetime string in ISO format (e.g., '2024-12-18 19:25').
        If the input format is invalid, returns the original string.
    """
    try:
        return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return dt_str  # Return as-is if the format is invalid

def to_datetime_local(dt_str):
    """
    Convert a datetime string from ISO format to HTML datetime-local format.

    Args:
        dt_str (str): The datetime string in ISO format (e.g., '2024-12-18 19:25').

    Returns:
        str: The datetime string in HTML datetime-local format (e.g., '2024-12-18T19:25').
        If the input format is invalid, returns the original string.
    """
    try:
        return datetime.strptime(dt_str, "%Y-%m-%d %H:%M").strftime("%Y-%m-%dT%H:%M")
    except ValueError:
        return dt_str  # Return as-is if the format is invalid

def calculate_date_range(range_option):
    """
    Calculate the start and end date based on the range option.

    Args:
        range_option (str): One of 'last_week', 'last_month', or 'all_time'.

    Returns:
        tuple: A start date (or None for all_time) and an end date.
    """
    now = datetime.now()
    if range_option == 'last_week':
        start_date = (now - timedelta(days=7)).strftime('%Y-%m-%d 00:00:00')  # Start of 7 days ago
        end_date = now.strftime('%Y-%m-%d 23:59:59')  # End of today
    elif range_option == 'last_month':
        start_date = (now - timedelta(days=30)).strftime('%Y-%m-%d 00:00:00')  # Start of 30 days ago
        end_date = now.strftime('%Y-%m-%d 23:59:59')  # End of today
    else:
        start_date = None  # No start date for 'all_time'
        end_date = None    # No end date for 'all_time'

    return start_date, end_date

