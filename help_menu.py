"""
Module: help_menu.py
Purpose: Prints available commands and functional usage hints.
"""

def display_help() -> None:
    """Prints the command catalog."""
    menu = """
-------------------- MINI ALEXA COMMANDS --------------------
Type any of the following command keywords:

  time          -> Display current system time
  date          -> Display today's date
  calculate     -> Perform arithmetic (e.g., 'calculate 15 * 4')
  quote         -> Get an inspiring motivational quote
  joke          -> Hear a tech/developer joke
  fact          -> Read an AI/tech fact
  game          -> Play number guessing challenge
  recommend     -> Rule-based activity recommendation (AI Concept)
  perceptron    -> Single neuron forward pass simulation (DL Concept)
  help          -> Show this menu
  exit          -> Terminate session
-------------------------------------------------------------
"""
    print(menu)