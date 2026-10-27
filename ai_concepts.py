"""
Module: ai_concepts.py
Purpose: Explicit pedagogical demonstrations of AI, ML, and DL fundamentals using native Python.
Requirements: FR-13 (Rule-Based Decision System) & FR-14 (Perceptron Simulation).
"""

from datetime_utils import get_current_hour

def recommend_activity() -> str:
    """
    Demonstrates Rule-Based AI Decision Making (Decision Tree Analogy).
    Evaluates current time conditions to recommend contextual activities.
    """
    hour = get_current_hour()

    if 5 <= hour < 12:
        return "Assistant [AI Rule Engine]: Good morning! Recommended activity: Morning focus work, plan your goals, and hydrate."
    elif 12 <= hour < 14:
        return "Assistant [AI Rule Engine]: Midday update: Recommended activity: Have a balanced lunch and take a 10-minute mental break."
    elif 14 <= hour < 18:
        return "Assistant [AI Rule Engine]: Afternoon sprint: Recommended activity: Deep coding session, debugging, and project review."
    elif 18 <= hour < 22:
        return "Assistant [AI Rule Engine]: Evening wind-down: Recommended activity: Exercise, read technical articles, and relax."
    else:
        return "Assistant [AI Rule Engine]: Late night: Recommended activity: Sleep and rest your brain for high cognitive retention tomorrow."

def perceptron_demo() -> None:
    """
    Demonstrates Deep Learning Neuron Fundamentals (Perceptron):
    Formula: z = (x1 * w1) + (x2 * w2) + bias
    Activation: Step Function -> 1 if z >= 0 else 0
    """
    print("\n" + "=" * 50)
    print("      DEEP LEARNING CONCEPT DEMO: PERCEPTRON")
    print("=" * 50)
    print("An Artificial Neuron computes: Output = Activation(Sum(Input * Weight) + Bias)")
    print("Fixed Weights: w1 = 0.6, w2 = 0.4 | Fixed Bias = -0.5 | Activation: Step at 0\n")

    try:
        x1 = float(input("Enter input value x1 (e.g., 1 or 0): ").strip())
        x2 = float(input("Enter input value x2 (e.g., 1 or 0): ").strip())
    except ValueError:
        print("Assistant: Invalid numeric inputs. Demo cancelled.\n")
        return

    # Fixed Parameters
    w1, w2 = 0.6, 0.4
    bias = -0.5

    # Forward Propagation Step
    weighted_sum = (x1 * w1) + (x2 * w2) + bias

    # Step Activation Function
    activation_output = 1 if weighted_sum >= 0 else 0

    print(f"\n[Forward Pass Computations]:")
    print(f" -> Input vector (X): [{x1}, {x2}]")
    print(f" -> Linear combination (Z): ({x1} * {w1}) + ({x2} * {w2}) + ({bias}) = {weighted_sum:.3f}")
    print(f" -> Step Activation Result: {activation_output} (Neuron {'Fired / Active' if activation_output == 1 else 'Inactive'})\n")