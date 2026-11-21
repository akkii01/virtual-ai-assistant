"""
Module: web_app.py
Project: Virtual AI Assistant (Mini Alexa - Web & Voice Edition)
Author: Akshit Raj
Description: Flask web server wrapping the existing modular console assistant
             with a live browser UI/UX, Voice I/O, Wikipedia Knowledge Engine,
             Persistent Task Manager + Focus Timer, and Offline NLP Analyzer.
"""

import io
import re
import math
import random
from contextlib import redirect_stdout
from flask import Flask, render_template, request, jsonify

# Import existing console modules without modifying them
from greetings import build_welcome_message, build_farewell_message
from datetime_utils import get_current_date, get_current_time
from calculator import calculate
from content import get_random_quote, get_random_joke, get_random_fact
from ai_concepts import recommend_activity
from help_menu import display_help

# Import 3-in-1 offline/API-free smart features (untouched)
from smart_features import KnowledgeEngine, TaskAndTimerManager, OfflineNLPEngine

app = Flask(__name__)

# Server-side session memory for web users
session_state = {
    "user_name": None,
    "game_active": False,
    "secret_number": None,
    "attempts_left": 0
}

# Initialize smart engines
wiki_engine = KnowledgeEngine()
task_timer_manager = TaskAndTimerManager()
nlp_engine = OfflineNLPEngine()


def capture_printed_output(func, *args, **kwargs) -> str:
    """Captures console print() output from existing modules so they render cleanly in Web UI."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        func(*args, **kwargs)
    return buffer.getvalue().strip()


def normalize_input(raw_input: str) -> str:
    return raw_input.strip().lower()


def clean_user_name(raw_text: str) -> str:
    """Extracts a clean user name, stripping greetings, wake words, and trailing questions."""
    cleaned = raw_text.strip()

    cleaned = re.sub(
        r"\b(how are you|how r u|how's it going|how is it going|nice to meet you|what's up|whats up|good morning|good afternoon|good evening|and you)\b.*$",
        "",
        cleaned,
        flags=re.IGNORECASE
    ).strip(" ,.!?")

    intro_match = re.search(
        r"(?:my name is|change my name to|call me|this is|it's|its|i am|i'm)\s+([a-zA-Z\s]+)$",
        cleaned,
        flags=re.IGNORECASE
    )
    if intro_match:
        cleaned = intro_match.group(1).strip()
    else:
        cleaned = re.sub(r"^(?:hi|hello|hey|no|mini alexa|alexa)\s+", "", cleaned, flags=re.IGNORECASE).strip()
        cleaned = re.sub(r"^(?:mini alexa|alexa)\s+", "", cleaned, flags=re.IGNORECASE).strip()

    cleaned = re.sub(r"\b(akshat|akshith|axit|akshit|accept|akshar)\b", "Akshit", cleaned, flags=re.IGNORECASE)

    words = cleaned.split()
    if len(words) >= 3 and words[0].lower() == words[-1].lower():
        words = words[:-1]
    cleaned = " ".join(words[:3])

    return cleaned.title() if cleaned else "Friend"


def is_math_query(text: str) -> bool:
    if "calculate" in text:
        return True
    if re.search(r'\d+\s*[\+\-\*\/]\s*\d+', text):
        return True
    return False


def run_web_perceptron_demo(raw_text: str) -> dict:
    """Non-blocking single-neuron Perceptron forward-pass simulation for Web & Voice UI."""
    nums = [float(n) for n in re.findall(r"-?\d+(?:\.\d+)?", raw_text)]
    x1 = nums[0] if len(nums) >= 1 else 0.8
    x2 = nums[1] if len(nums) >= 2 else 0.5
    w1, w2, bias = 0.6, 0.4, -0.3

    weighted_sum = round((x1 * w1) + (x2 * w2) + bias, 4)
    step_output = 1 if weighted_sum >= 0 else 0
    sigmoid_output = round(1 / (1 + math.exp(-weighted_sum)), 4)
    status = "ACTIVATED (1)" if step_output == 1 else "INACTIVE (0)"

    report = (
        "🧠 SINGLE-NEURON PERCEPTRON SIMULATION (FORWARD PASS)\n"
        f"{'-' * 52}\n"
        f"• Inputs         : x1 = {x1},  x2 = {x2}\n"
        f"• Weights & Bias : w1 = {w1},  w2 = {w2},  b = {bias}\n"
        f"• Weighted Sum   : z = ({x1} × {w1}) + ({x2} × {w2}) + ({bias}) = {weighted_sum}\n"
        f"• Step Activation: {status}  (Threshold ≥ 0)\n"
        f"• Sigmoid Prob.  : {sigmoid_output}\n"
        f"{'-' * 52}\n"
        "Tip: You can also pass custom inputs like 'perceptron 0.2 0.1'"
    )
    spoken = (
        f"Perceptron forward pass complete. With inputs {x1} and {x2}, "
        f"the weighted sum is {weighted_sum}, so the neuron is {'activated with output 1' if step_output == 1 else 'inactive with output 0'}."
    )
    return {"reply": report, "speak": spoken, "is_code": True}


def handle_web_game(command: str, user_name: str) -> str:
    """Handles stateful 5-try number guessing game cleanly over HTTP requests."""
    if any(k in command for k in ["quit", "exit", "stop", "cancel"]):
        session_state["game_active"] = False
        return f"Game cancelled, {user_name}. What else can I help you with?"

    try:
        guess = int(re.search(r'\d+', command).group())
    except (AttributeError, ValueError):
        return f"Please enter a valid number between 1 and 50, {user_name} (or type 'stop' to exit the game)."

    if guess < 1 or guess > 50:
        return "Number out of range! Guess a number between 1 and 50."

    session_state["attempts_left"] -= 1
    secret = session_state["secret_number"]

    if guess == secret:
        session_state["game_active"] = False
        return f"🎉 Congratulations {user_name}! You guessed the secret number {secret}!"

    if session_state["attempts_left"] == 0:
        session_state["game_active"] = False
        return f"Game Over, {user_name}! Out of attempts. The secret number was {secret}."

    hint = "Too low! Try a higher number." if guess < secret else "Too high! Try a lower number."
    return f"{hint} ({session_state['attempts_left']} attempts remaining)"


def process_web_command(raw_text: str) -> dict:
    """Deterministic intent router for console utilities + 3 advanced smart features."""
    cleaned = raw_text.strip()
    if not cleaned:
        return {"reply": "Please say or type a command.", "speak": "Please say or type a command."}

    # Step 1: Onboarding User Name if not set yet
    if not session_state["user_name"]:
        user_name = clean_user_name(cleaned)
        session_state["user_name"] = user_name
        welcome = build_welcome_message(user_name)
        return {"reply": welcome, "speak": welcome, "user_name": user_name}

    user_name = session_state["user_name"]
    command = normalize_input(cleaned)

    # Allow updating user name anytime
    if any(phrase in command for phrase in ["my name is", "change my name", "call me"]):
        new_name = clean_user_name(cleaned)
        session_state["user_name"] = new_name
        msg = f"Got it! I've updated your name to {new_name}. How can I help you?"
        return {"reply": msg, "speak": msg, "user_name": new_name}

    # Step 2: Check if Number Guessing Game is currently active
    if session_state["game_active"]:
        reply = handle_web_game(command, user_name)
        return {"reply": reply, "speak": reply}

    # Step 3: Offline NLP Summarizer & Sentiment Analyzer
    if any(command.startswith(prefix) for prefix in ["summarize", "summary", "analyze", "sentiment", "nlp"]):
        return nlp_engine.analyze_and_summarize(cleaned)

    # Step 4: Persistent Task Manager & Focus Timer (with Pause / Resume / Stop)
    if any(k in command for k in ["add task", "new task", "create task", "remind me to", "add to my list"]):
        return task_timer_manager.add_task(cleaned)

    elif any(k in command for k in ["show task", "show my task", "my task", "list task", "to do list", "todo list", "tasks"]):
        if any(w in command for w in ["complete", "done", "finish"]):
            return task_timer_manager.complete_task(cleaned)
        elif any(w in command for w in ["delete", "remove", "clear"]):
            return task_timer_manager.delete_task(cleaned)
        return task_timer_manager.list_tasks()

    elif any(k in command for k in ["complete task", "done task", "finish task"]):
        return task_timer_manager.complete_task(cleaned)

    elif any(k in command for k in ["delete task", "remove task", "clear all task"]):
        return task_timer_manager.delete_task(cleaned)

    elif any(k in command for k in ["pause timer", "pause focus", "pause the timer"]):
        return {"reply": "⏸️ Focus timer paused.", "speak": "Focus timer paused.", "timer_action": "pause"}

    elif any(k in command for k in ["resume timer", "continue timer", "unpause timer", "resume focus"]):
        return {"reply": "▶️ Focus timer resumed.", "speak": "Focus timer resumed.", "timer_action": "resume"}

    elif any(k in command for k in ["timer", "pomodoro", "countdown", "focus mode"]):
        return task_timer_manager.parse_timer_request(cleaned)

    # Step 5: Core Console Utilities (Exact Priority Order)
    if any(k in command for k in ["exit", "quit", "bye", "terminate", "stop"]):
        farewell = build_farewell_message(user_name)
        session_state["user_name"] = None
        return {"reply": farewell, "speak": farewell, "reset": True}

    elif any(k in command for k in ["help", "menu", "command", "commands"]):
        base_help = capture_printed_output(display_help)
        extra_help = (
            "\n\n🚀 SMART WEB & VOICE FEATURES:\n"
            "  • Wikipedia Lookup : 'Tell me about baclofen within 100 words' / 'What is AI?'\n"
            "  • Task Manager     : 'Add task [name]' | 'My tasks' | 'Complete task 1'\n"
            "  • Focus Timer      : 'Start 25 minute timer' | 'Pause timer' | 'Resume timer' | 'Stop timer'\n"
            "  • NLP Analyzer     : 'Summarize: [paragraph]' | 'Analyze: [text]'"
        )
        spoken_commands = (
            "Here are all the commands you can ask me: "
            "Time, Date, Calculate, Quote, Joke, Fact, Game, Recommend, Perceptron, Help, and Exit. "
            "Plus four smart features: Wikipedia Lookup for any topic in short, detailed, or exact word counts; "
            "Task Manager to add, view, or complete tasks; Focus Timer with pause, resume, and stop controls; "
            "and Offline NLP Analyzer to summarize or check the tone of any text."
        )
        return {
            "reply": base_help + extra_help,
            "speak": spoken_commands,
            "is_code": True
        }

    elif "date" in command:
        res = get_current_date()
        return {"reply": res, "speak": res}

    elif "time" in command:
        res = get_current_time()
        return {"reply": res, "speak": res}

    elif any(k in command for k in ["quote", "motivation", "motivational", "inspire", "inspiring"]):
        res = get_random_quote(user_name)
        return {"reply": res, "speak": res}

    elif any(k in command for k in ["joke", "jokes", "funny", "humor"]):
        res = get_random_joke()
        return {"reply": res, "speak": res}

    elif any(k in command for k in ["fact", "facts", "knowledge"]):
        res = get_random_fact()
        return {"reply": res, "speak": res}

    elif any(k in command for k in ["game", "guess", "play"]):
        session_state["game_active"] = True
        session_state["secret_number"] = random.randint(1, 50)
        session_state["attempts_left"] = 5
        msg = f"🎮 Number Guessing Game Started, {user_name}! I have chosen a secret number between 1 and 50. You have 5 attempts. Enter your first guess!"
        return {"reply": msg, "speak": f"Number guessing game started, {user_name}. Guess a number between 1 and 50."}

    elif any(k in command for k in ["recommend", "activity", "suggest", "suggestion", "schedule"]):
        res = recommend_activity()
        return {"reply": res, "speak": res}

    elif any(k in command for k in ["perceptron", "neuron", "neural", "deep learning", "forward pass"]):
        return run_web_perceptron_demo(cleaned)

    elif is_math_query(command):
        res = calculate(command)
        return {"reply": res, "speak": res}

    # Step 6: Universal Wikipedia Knowledge Lookup (untouched)
    elif (
        any(k in command for k in ["tell me about", "what is", "what are", "who is", "who was", "define", "explain", "search", "wiki"])
        or re.search(r"\b(\d{1,5}\s+words?|in\s+detail|in\s+short|in\s+brief|in\s+medium)\b", command)
    ):
        return wiki_engine.lookup(cleaned)

    else:
        fallback = f"Assistant: I'm not sure I understood that, {user_name}. Say or type 'help' to see all commands, or ask 'Tell me about [any topic]'."
        return {"reply": fallback, "speak": f"I'm not sure I understood that, {user_name}. Say help to see what I can do."}


@app.route("/")
def index():
    session_state["user_name"] = None
    session_state["game_active"] = False
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")
    response_data = process_web_command(user_message)
    return jsonify(response_data)


if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("  MINI ALEXA - WEB & VOICE EDITION IS LIVE!")
    print("  Open in Chrome/Edge: http://127.0.0.1:5000")
    print("=" * 55 + "\n")
    app.run(debug=True, port=5000)