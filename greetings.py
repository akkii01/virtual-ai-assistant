"""
Module: greetings.py
Purpose: Handles user onboarding, session name capture, and greeting logic.
AI Concept: Human-Computer Interaction (HCI) initialization and session memory.
"""

def get_user_name() -> str:
    """Prompt the user for their name and sanitize input."""
    while True:
        name = input("Assistant: Hi! I'm Mini Alexa. What's your name?\nYou: ").strip()
        if name:
            return name.title()
        print("Assistant: I didn't catch that. Please enter a valid name.\n")

def build_welcome_message(user_name: str) -> str:
    """Return a personalized welcome message."""
    return f"Assistant: Nice to meet you, {user_name}! Type 'help' to see what I can do.\n"

def build_farewell_message(user_name: str) -> str:
    """Return a personalized exit message."""
    return f"\nAssistant: Goodbye, {user_name}! Have a productive day ahead."