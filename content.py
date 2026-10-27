"""
Module: content.py
Purpose: Predefined knowledge base for quotes, jokes, and facts.
AI/ML Analogy: Content repository & simplified heuristic recommendation.
"""

import random

QUOTES = [
    "The secret of getting ahead is getting started. – Mark Twain",
    "It always seems impossible until it's done. – Nelson Mandela",
    "Programs must be written for people to read, and only incidentally for machines to execute. – Harold Abelson",
    "Simplicity is prerequisite for reliability. – Edsger W. Dijkstra",
    "The best way to predict the future is to invent it. – Alan Kay"
]

JOKES = [
    "Why did the developer go broke? Because they used up all their cache.",
    "There are 10 types of people in the world: those who understand binary, and those who don't.",
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "An SQL query walks into a bar, walks up to two tables and asks, 'Can I join you?'",
    "A bug is never just a mistake. It represents something bigger: an error of understanding."
]

FACTS = [
    "The first computer bug was an actual real-life moth stuck in a Harvard Mark II computer in 1947.",
    "Python was conceived in the late 1980s by Guido van Rossum and named after Monty Python's Flying Circus.",
    "The first artificial neural network was the Perceptron, invented in 1958 by Frank Rosenblatt.",
    "More than 80% of current AI workloads rely heavily on Python standard paradigms and vectorized pipelines.",
    "The term 'Artificial Intelligence' was coined at the Dartmouth Workshop in 1956."
]

def get_random_quote(user_name: str) -> str:
    return f"Assistant: Here is a quote for you, {user_name}:\n\"{random.choice(QUOTES)}\""

def get_random_joke() -> str:
    return f"Assistant: {random.choice(JOKES)}"

def get_random_fact() -> str:
    return f"Assistant: Did you know? {random.choice(FACTS)}"