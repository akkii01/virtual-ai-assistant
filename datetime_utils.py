"""
Module: datetime_utils.py
Purpose: Fetches and formats system date and time.
Python Concepts: datetime module, strftime formatting.
"""

from datetime import datetime

def get_current_date() -> str:
    """Returns formatted system date."""
    now = datetime.now()
    return f"Assistant: Today's date is {now.strftime('%A, %B %d, %Y')}."

def get_current_time() -> str:
    """Returns formatted system time."""
    now = datetime.now()
    return f"Assistant: It's currently {now.strftime('%I:%M %p')}."

def get_current_hour() -> int:
    """Helper function to fetch the current 24-hour cycle hour."""
    return datetime.now().hour