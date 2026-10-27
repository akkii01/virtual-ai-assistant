"""
Module: calculator.py
Purpose: Parses arithmetic inputs safely without relying on unsafe eval().
Python Concepts: String parsing, Regular Expressions, ZeroDivisionError.
"""

import re

def calculate(user_input: str) -> str:
    """
    Parses and calculates expressions containing +, -, *, /
    Supports both direct arithmetic ('15 * 4') and prefixed queries ('calculate 876/70').
    """
    cleaned = user_input.lower().replace("calculate", "").strip()

    # Match exact arithmetic pattern: number operator number
    match = re.search(r'(-?\d+(?:\.\d+)?)\s*([\+\-\*\/])\s*(-?\d+(?:\.\d+)?)', cleaned)
    
    if not match:
        return "Assistant: Please provide a valid operation with two numbers (e.g., 'calculate 15 * 4' or '876 / 70')."

    num1_str, op, num2_str = match.groups()

    try:
        num1 = float(num1_str)
        num2 = float(num2_str)

        if op == "+":
            res = num1 + num2
        elif op == "-":
            res = num1 - num2
        elif op == "*":
            res = num1 * num2
        elif op == "/":
            if num2 == 0:
                return "Assistant: I can't divide by zero — try a different number."
            res = num1 / num2

        if res.is_integer():
            res = int(res)

        return f"Assistant: The result is {res}"

    except ValueError:
        return "Assistant: Invalid numbers detected. Please use digits only."