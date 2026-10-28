"""
Module: content.py
Purpose: Predefined knowledge base for quotes, jokes, and facts.
AI/ML Analogy: Content repository & simplified heuristic recommendation.
"""

import random

import random

QUOTES = [
    "It always seems impossible until it's done. – Nelson Mandela",
    "Simplicity is prerequisite for reliability. – Edsger W. Dijkstra",
    "The secret of getting ahead is getting started. – Mark Twain",
    "The best way to predict the future is to invent it. – Alan Kay",
    "Programs must be written for people to read, and only incidentally for machines to execute. – Harold Abelson",
    "Any fool can write code that a computer can understand. Good programmers write code that humans can understand. – Martin Fowler",
    "First, solve the problem. Then, write the code. – John Johnson",
    "Experience is the name everyone gives to their mistakes. – Oscar Wilde",
    "Talk is cheap. Show me the code. – Linus Torvalds",
    "Code is like humor. When you have to explain it, it’s bad. – Cory House"
]

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "Why did the developer go broke? Because they used up all their cache.",
    "There are 10 types of people in the world: those who understand binary, and those who don't.",
    "An SQL query walks into a bar, walks up to two tables and asks, 'Can I join you?'",
    "A bug is never just a mistake. It represents something bigger: an error of understanding.",
    "Why do Java programmers have to wear glasses? Because they don't C#.",
    "Real programmers count from 0.",
    "Hardware is made to be hit when software breaks down."
]

FACTS = [
    "The term 'Artificial Intelligence' was coined at the Dartmouth Workshop in 1956.",
    "The first computer bug was an actual real-life moth stuck in a Harvard Mark II computer in 1947.",
    "The first artificial neural network was the Perceptron, invented in 1958 by Frank Rosenblatt.",
    "Python was conceived in the late 1980s by Guido van Rossum and named after Monty Python's Flying Circus.",
    "More than 80% of current AI workloads rely heavily on Python standard paradigms and vectorized pipelines.",
    "Ada Lovelace is regarded as the world's first computer programmer for her work on the Analytical Engine in 1843.",
    "The world's first 1 GB hard drive was released by IBM in 1980 and weighed over 500 pounds.",
    "Over 700 programming languages exist today, but Python remains the most popular for AI and ML."
]

# Track last served content to avoid immediate repetitions
_last_quote = None
_last_joke = None
_last_fact = None

def get_quote():
    global _last_quote
    choices = [q for q in QUOTES if q != _last_quote]
    _last_quote = random.choice(choices)
    return _last_quote

def get_joke():
    global _last_joke
    choices = [j for j in JOKES if j != _last_joke]
    _last_joke = random.choice(choices)
    return _last_joke

def get_fact():
    global _last_fact
    choices = [f for f in FACTS if f != _last_fact]
    _last_fact = random.choice(choices)
    return _last_fact