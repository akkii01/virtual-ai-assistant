"""
Module: main.py
Project: Virtual AI Assistant (Mini Alexa)
Track: Nexbridge Technologies AI Internship Program
Author: Akshit Raj
Description: Entry point and execution loop for rule-based virtual assistant.
"""

import sys
import re
from greetings import get_user_name, build_welcome_message, build_farewell_message
from datetime_utils import get_current_date, get_current_time
from calculator import calculate
from content import get_random_quote, get_random_joke, get_random_fact
from game import play_guessing_game
from ai_concepts import recommend_activity, perceptron_demo
from help_menu import display_help

def normalize_input(raw_input: str) -> str:
    """Strips leading/trailing whitespace and normalizes to lowercase."""
    return raw_input.strip().lower()

def is_math_query(text: str) -> bool:
    """
    Check if the input is explicitly a math command or a numeric arithmetic expression.
    Prevents false triggers from words with hyphens ('step-by-step') or slashes ('and/or').
    """
    if "calculate" in text:
        return True
    # Match patterns like: digit + operator + digit (e.g., '12 + 8', '5/2', '10 - 4')
    if re.search(r'\d+\s*[\+\-\*\/]\s*\d+', text):
        return True
    return False

def route_command(command: str, user_name: str) -> bool:
    """
    Pattern matching & keyword detection engine.
    Routes user intent to functional modules. Returns False if session exits.
    """
    # FR-11: Exit Handler (checked first)
    if any(k in command for k in ["exit", "quit", "bye", "terminate", "stop"]):
        print(build_farewell_message(user_name))
        return False

    # FR-10: Help
    elif any(k in command for k in ["help", "menu", "command", "commands"]):
        display_help()

    # FR-03: Date
    elif "date" in command:
        print(get_current_date())

    # FR-04: Time
    elif "time" in command:
        print(get_current_time())

    # FR-06: Quotes
    elif any(k in command for k in ["quote", "motivation", "motivational", "inspire", "inspiring"]):
        print(get_random_quote(user_name))

    # FR-07: Jokes
    elif any(k in command for k in ["joke", "jokes", "funny", "humor"]):
        print(get_random_joke())

    # FR-08: Facts
    elif any(k in command for k in ["fact", "facts", "knowledge"]):
        print(get_random_fact())

    # FR-09: Number Guessing Game
    elif any(k in command for k in ["game", "guess", "play"]):
        play_guessing_game(user_name)

    # FR-13: Rule-Based Recommendation
    elif any(k in command for k in ["recommend", "activity", "suggest", "suggestion", "schedule"]):
        print(recommend_activity())

    # FR-14: Perceptron Deep Learning Demo
    elif any(k in command for k in ["perceptron", "neuron", "neural", "deep learning"]):
        perceptron_demo()

    # FR-05: Calculator (handled after exit/general keywords)
    elif is_math_query(command):
        print(calculate(command))

    # FR-12: Fallback Handler
    else:
        print(f"Assistant: I'm not sure I understood that, {user_name}. Type 'help' to see what I can do.")

    print() # Clean terminal line break
    return True

def main():
    print("=" * 55)
    print("      MINI ALEXA - VIRTUAL ASSISTANT (CONSOLE EDITION)")
    print("=" * 55)

    # FR-01 & FR-02: User Name & Greeting initialization
    user_name = get_user_name()
    print(build_welcome_message(user_name))

    # Continuous conversational loop
    is_running = True
    while is_running:
        try:
            raw_input = input(f"{user_name}: ")
            normalized = normalize_input(raw_input)
            
            if not normalized:
                continue

            is_running = route_command(normalized, user_name)

        except (KeyboardInterrupt, EOFError):
            print(build_farewell_message(user_name))
            break
        except Exception as error:
            print(f"Assistant: An unexpected runtime error occurred: {error}")

if __name__ == "__main__":
    main()