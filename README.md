# Virtual AI Assistant (Mini Alexa)

A modular, console-based virtual assistant built entirely using Python 3 and the standard library. Developed as part of the Nexbridge Technologies AI Internship Program (Project Code: AI-INT-P1-VAA).

---

## Repository
- **GitHub Repository**: [https://github.com/akkii01/virtual-ai-assistant](https://github.com/akkii01/virtual-ai-assistant)
- **Author**: Akshit Raj
- **Track**: Artificial Intelligence — Beginner Track

---

## Project Highlights
- **100% Offline & Pure Python**: Operates using Python Standard Library modules (`random`, `datetime`, `re`, `sys`) with zero external pip dependencies.
- **Resilient & Crash-Proof**: Defensive exception handling (`try-except`) across mathematical parsing, command routing, and interactive loops to prevent edge-case failures.
- **Modular Architecture**: Clean functional separation across dedicated modules following professional code standards.
- **Pedagogical AI/ML/DL Demonstrations**:
  - **Rule-Based Reasoning**: Context-aware activity recommendations based on temporal input (Decision Tree analogy).
  - **Single Artificial Neuron (Perceptron)**: Mathematical simulation of forward propagation computing weighted inputs, bias, and step activation ($Z = \sum W_i X_i + b$).

---

## Project Structure
```
virtual-ai-assistant/
│── main.py            # Program entry point and intent dispatch loop
│── greetings.py       # User onboarding and session state management
│── datetime_utils.py  # System time and date retrieval utilities
│── calculator.py      # Resilient arithmetic expression parser
│── content.py         # Knowledge repository for quotes, jokes, and tech facts
│── game.py            # Stateful number-guessing game with attempt tracking
│── ai_concepts.py     # Rule-based decision engine and Perceptron simulation
│── help_menu.py       # Formatted command catalog and interactive guide
└── README.md          # Complete project documentation
```

## Installation & Setup

Clone the repository:
```
Bash

git clone [https://github.com/akkii01/virtual-ai-assistant.git](https://github.com/akkii01/virtual-ai-assistant.git)
```
Navigate to the project directory:
```
Bash

cd virtual-ai-assistant
```
Run the assistant:
```
Bash

python main.py
```

## Command Catalog
Command TriggerDescriptionConcept DemonstratedtimeReturns the current formatted system time   Python datetime formatting   dateReturns today's full date   Python datetime formatting   calculate <n1> <op> <n2>Safely evaluates arithmetic expressions (+, -, *, /)   Regex parsing & defensive arithmetic   quoteDelivers randomized motivational wisdom   Random sampling heuristic   jokeDelivers randomized tech/developer humor   Random selection from corpus[cite: 6]factDisplays an AI/Computer Science history fact[cite: 6]Information retrieval analogy[cite: 6]gameInitiates the 5-try number guessing challenge[cite: 6]Stateful loop & conditional logic[cite: 6]recommendContext-aware schedule recommendation[cite: 6]Rule-based AI / Decision Tree[cite: 6]perceptronForward propagation pass of a single neuron[cite: 6]Deep Learning neuron & Step activation[cite: 6]helpDisplays the command catalog[cite: 6]User assistance interface[cite: 6]exit / quitGracefully closes the session[cite: 6]Lifecycle & graceful termination[cite: 6]

## Verification & Testing
The project satisfies all functional requirements (FR-01 through FR-14) outlined in the Nexbridge Technologies PRD[cite: 6]:

Handles malformed expressions and zero-division errors gracefully[cite: 6].

Retains user identity dynamically within active session memory[cite: 6].

Executes 100% offline with zero external runtime packages[cite: 6].
