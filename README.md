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

git clone https://github.com/akkii01/virtual-ai-assistant.git
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

<table>
  <thead>
    <tr>
      <th align="left">Command Trigger</th>
      <th align="left">Description</th>
      <th align="left">Concept Demonstrated</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>time</code></td>
      <td>Returns the current formatted system time</td>
      <td>Python <code>datetime</code> formatting</td>
    </tr>
    <tr>
      <td><code>date</code></td>
      <td>Returns today's full date</td>
      <td>Python <code>datetime</code> formatting</td>
    </tr>
    <tr>
      <td><code>calculate &lt;n1&gt; &lt;op&gt; &lt;n2&gt;</code></td>
      <td>Safely evaluates arithmetic expressions (<code>+</code>, <code>-</code>, <code>*</code>, <code>/</code>)</td>
      <td>Regex parsing &amp; defensive arithmetic</td>
    </tr>
    <tr>
      <td><code>quote</code></td>
      <td>Delivers randomized motivational wisdom</td>
      <td>Random sampling heuristic</td>
    </tr>
    <tr>
      <td><code>joke</code></td>
      <td>Delivers randomized tech/developer humor</td>
      <td>Random selection from corpus</td>
    </tr>
    <tr>
      <td><code>fact</code></td>
      <td>Displays an AI/Computer Science history fact</td>
      <td>Information retrieval analogy</td>
    </tr>
    <tr>
      <td><code>game</code></td>
      <td>Initiates the 5-try number guessing challenge</td>
      <td>Stateful loop &amp; conditional logic</td>
    </tr>
    <tr>
      <td><code>recommend</code></td>
      <td>Context-aware schedule recommendation</td>
      <td>Rule-based AI / Decision Tree</td>
    </tr>
    <tr>
      <td><code>perceptron</code></td>
      <td>Forward propagation pass of a single neuron</td>
      <td>Deep Learning neuron &amp; Step activation</td>
    </tr>
    <tr>
      <td><code>help</code></td>
      <td>Displays the command catalog</td>
      <td>User assistance interface</td>
    </tr>
    <tr>
      <td><code>exit</code> / <code>quit</code></td>
      <td>Gracefully closes the session</td>
      <td>Lifecycle &amp; graceful termination</td>
    </tr>
  </tbody>
</table>

## Verification & Testing
The project satisfies all functional requirements (FR-01 through FR-14) outlined in the Nexbridge Technologies PRD[cite: 6]:

Handles malformed expressions and zero-division errors gracefully[cite: 6].

Retains user identity dynamically within active session memory[cite: 6].

Executes 100% offline with zero external runtime packages[cite: 6].
