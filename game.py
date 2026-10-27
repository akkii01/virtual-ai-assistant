"""
Module: game.py
Purpose: Interactive number guessing game demonstrating loops, states, and condition checks.
"""

import random

def play_guessing_game(user_name: str) -> None:
    """Runs a 5-attempt number guessing game between 1 and 20."""
    secret_number = random.randint(1, 20)
    attempts_left = 5

    print(f"\nAssistant: I'm thinking of a number between 1 and 20. You have {attempts_left} tries, {user_name}!")

    while attempts_left > 0:
        guess_str = input(f"Guess a number ({attempts_left} tries remaining): ").strip()
        
        # Validate integer input
        try:
            guess = int(guess_str)
        except ValueError:
            print("Assistant: Please enter a valid integer between 1 and 20.")
            continue

        if guess < 1 or guess > 20:
            print("Assistant: Stay within the range 1 to 20.")
            continue

        if guess == secret_number:
            print(f"Assistant: Spot on, {user_name}! You guessed the number {secret_number} correctly!\n")
            return
        elif guess < secret_number:
            print("Assistant: Higher!")
        else:
            print("Assistant: Lower!")

        attempts_left -= 1

    print(f"Assistant: Game over! The secret number was {secret_number}. Better luck next time!\n")