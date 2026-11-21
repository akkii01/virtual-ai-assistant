# Virtual AI Assistant (Mini Alexa)

A modular, API-key-free virtual AI assistant built with Python 3—available in both a **Zero-Dependency Console Edition** and an interactive **Flask Web & Voice Edition**. Developed as part of the Nexbridge Technologies AI Internship Program (Project Code: AI-INT-P1-VAA).

---

## Repository
- **GitHub Repository**: [https://github.com/akkii01/virtual-ai-assistant](https://github.com/akkii01/virtual-ai-assistant)
- **Author**: Akshit Raj
- **Track**: Artificial Intelligence — Beginner Track

---

## Project Highlights
- **Dual-Mode Execution**:
  - **Console Edition (`main.py`)**: 100% offline using only Python Standard Library modules (`random`, `datetime`, `re`, `sys`) with zero external dependencies.
  - **Web & Voice Edition (`web_app.py`)**: Modern Flask web interface with browser-based Voice Input (`SpeechRecognition`), continuous sentence-chunked Text-to-Speech (`speechSynthesis`) to prevent cutoff on long outputs, and quick-action command chips.
- **Zero API Keys Required**: Every smart feature operates using pure Python logic or free public endpoints—no paid keys or authentication setup required.
- **3-in-1 Smart Web & Voice Modules (`smart_features.py`)**:
  - **Universal Wikipedia Knowledge Engine**: Smart exact-title resolution, tech acronym mapping (`RAG`, `NLP`, `LLM`), and dynamic length control (short, medium, detailed, or exact target word counts from 20 to 10,000 words).
  - **Persistent Task Manager & Focus Timer**: Local JSON-backed To-Do list (`tasks.json`) and live browser countdown timer with **Pause**, **Resume**, and **Stop** controls plus voice alerts.
  - **Offline NLP Analyzer**: Pure Python extractive text summarization (word-frequency sentence scoring), negation-aware sentiment polarity analysis, keyword extraction, and reading time estimation.
- **Pedagogical AI/ML/DL Demonstrations**:
  - **Rule-Based Reasoning**: Context-aware activity recommendations based on temporal input (Decision Tree analogy).
  - **Single Artificial Neuron (Perceptron)**: Forward propagation simulation computing weighted inputs, bias, step activation ($Z = \sum W_i X_i + b$), and sigmoid probability (available in both console and non-blocking web modes).
- **Resilient & Crash-Proof**: Defensive exception handling (`try-except`) across mathematical parsing, API lookups, and interactive loops.

---

## Project Structure
```text
virtual-ai-assistant/
├── templates/
│   └── index.html       # Responsive Web UI, Voice I/O engine, and live Focus Timer
├── web_app.py           # Flask web server and unified command router (Web & Voice Edition)
├── smart_features.py    # Wikipedia engine, Task/Timer manager, and Offline NLP analyzer
├── main.py              # Console entry point and intent dispatch loop (Console Edition)
├── greetings.py         # User onboarding and session state management
├── datetime_utils.py    # System time and date retrieval utilities
├── calculator.py        # Resilient arithmetic expression parser
├── content.py           # Knowledge repository for quotes, jokes, and tech facts
├── game.py              # Stateful number-guessing game with attempt tracking
├── ai_concepts.py       # Rule-based decision engine and Perceptron simulation
├── help_menu.py         # Formatted command catalog and interactive guide
├── requirements.txt     # Python dependencies for Web & Voice Edition (Flask)
├── .gitignore           # Excludes local cache (__pycache__) and personal task data (tasks.json)
└── README.md            # Complete project documentation
```

Installation & Setup
## 1. Clone the repository:
```
git clone [https://github.com/akkii01/virtual-ai-assistant.git](https://github.com/akkii01/virtual-ai-assistant.git)
cd virtual-ai-assistant
```
## 1. Option A — Run the Console Edition (Zero Dependencies):
```
python main.py
```
## 1. Option B — Run the Web & Voice Edition (Recommended):
Install Flask:
```
pip install -r requirements.txt
```
## Start the local web server:
```
python web_app.py
```
Open http://127.0.0.1:5000 in Google Chrome or Microsoft Edge for full Voice Recognition and Text-to-Speech support.

## Command Catalog
Core Assistant Commands (Console & Web)
Smart Web & Voice Commands

## Verification & Testing

-  Satisfies all core functional requirements (FR-01 through FR-14) outlined in the Nexbridge Technologies PRD.

-  Handles malformed mathematical expressions, zero-division errors, and network timeouts gracefully without crashing.

-  Retains user identity dynamically within active session memory and cleans voice-transcribed names automatically.

-  Console mode runs 100% offline with zero external packages; Web & Voice edition runs locally with only Flask and zero API keys.