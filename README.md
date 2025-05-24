# Mental Health Support System

A multi-agent, multi-tool mental health support chatbot built using LangGraph, LangChain, and Streamlit.

---

## 📜 Table of Contents

* [Project Overview](#project-overview)
* [Example](#example-interactions)
* [Workflow](#workflow)
* [Features](#features)
* [Architecture](#architecture)
* [Workflow](#workflow)
* [Getting Started](#getting-started)

  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Configuration](#configuration)
  * [Running the Application](#running-the-application)
* [Project Structure](#project-structure)
* [Agents and Tools](#agents-and-tools)
* [Graph and State Management](#graph-and-state-management)
* [Streamlit Interface](#streamlit-interface)
* [Usage Guide](#usage-guide)
* [Development Roadmap](#development-roadmap)
* [Contributing](#contributing)
* [License](#license)

---

## 🌟 Project Overview

The **Mental Health Support System** is a conversational AI platform designed to provide empathetic and evidence-based mental health support. It utilizes a network of specialized agents, each with dedicated tools, to address a variety of mental health concerns, including crisis intervention, therapeutic support, resource coordination, and wellness coaching.

---

# Workflow


---

## Example Interactions



---

## ✨ Features

* **Multi-Agent Architecture:**

  * Includes Intake, Crisis, Therapeutic, Resource Coordinator, and Wellness Coach agents.
* **Tool Integration:**

  * Search tools, crisis resources, therapy exercises, wellness plans, and more.
* **Intelligent Routing:**

  * Dynamically routes users to the most appropriate agent based on context.
* **Stateful Conversations:**

  * Maintains session history and context throughout the interaction.
* **Modern UI:**

  * Built with Streamlit for an accessible and responsive interface.
* **Safety Focused:**

  * Detects and prioritizes crisis scenarios with immediate resource recommendations.

---

## 🏗️ Architecture

The system is constructed using:

* **LangGraph:** Manages agent routing and flow.
* **LangChain:** Integrates LLMs and toolkits.
* **Streamlit:** Provides the web interface.
* **Google Serper API:** Enables real-time resource searching.

---

## ⚙️ Workflow

1. **User Interaction**

   * **Command Line:** Via `main.py`.
   * **Web Interface:** Via `app.py`.

2. **Intake and Routing**

   * The **Intake Agent** initiates the session, assesses needs, and routes to the appropriate agent.

3. **Specialized Support**

   * **Crisis Agent:** Immediate help and safety planning.
   * **Therapeutic Agent:** Therapy and coping strategies.
   * **Resource Coordinator:** Connects to relevant resources.
   * **Wellness Coach:** Lifestyle and wellness tips.

4. **State Management**

   * Uses Graph Runner and Enhanced State for session tracking and routing.

5. **Modularity and Safety**

   * Modular agent and tool structure ensures maintainability.
   * Crisis detection ensures user safety.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.9+
* Git (optional)
* API Keys:

  * **Groq API Key**
  * **Google Serper API Key**

### Installation

1. Clone the repository (optional):

```bash
git clone https://github.com/yourusername/mental-health-support-system.git
cd mental-health-support-system
```

2. Create a virtual environment:

```bash
# Create and activate a virtual environment using uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate.bat or .venv\Scripts\Activate.ps1
```

3. Install dependencies using `uv` (recommended):

```bash
uv sync
```

### Configuration

1. Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key
SERPER_API_KEY=your_serper_api_key
MODEL_NAME=gemma2-9b-it
```

2. Replace the placeholders with your actual API credentials.

### Running the Application

* **Streamlit Web Interface:**

```bash
streamlit run app.py
```

* **Command Line Interface:**

```bash
python main.py
```

---

## 📂 Project Structure

```
mental-health-support-system/
├── agents/
│   ├── __init__.py
│   ├── intake_agent.py
│   ├── crisis_agent.py
│   ├── therapeutic_agent.py
│   ├── resource_coordinator_agent.py
│   └── wellness_coach_agent.py
├── tools/
│   ├── __init__.py
│   ├── search_tools.py
│   ├── crisis_tools.py
│   ├── therapeutic_tools.py
│   └── wellness_tools.py
├── states/
│   ├── __init__.py
│   └── enhanced_state.py
├── graphs/
│   ├── __init__.py
│   ├── graph_runner.py
│   └── main_graph.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── app.py
├── main.py
├── requirements.txt
└── README.md
```

---

## 🤖 Agents and Tools

### Agents

* **Intake Agent:** First point of contact, routes users.
* **Crisis Agent:** Handles emergencies and safety support.
* **Therapeutic Agent:** Offers exercises and psychological strategies.
* **Resource Coordinator:** Finds therapists and support services.
* **Wellness Coach:** Provides lifestyle and wellness advice.

### Tools

* **Search Tools:** Real-time web searches.
* **Crisis Tools:** Hotline and emergency planning resources.
* **Therapeutic Tools:** CBT, mindfulness, journaling.
* **Wellness Tools:** Nutrition, exercise, sleep guides.

---

## 🧩 Graph and State Management

* **Main Graph:** Directs flow between agents using LangGraph.
* **Graph Runner:** Handles lifecycle and session flow.
* **Enhanced State:** Stores user profile, conversation history, crisis level, and more.

---

## 🖥️ Streamlit Interface

* **Chat Interface:** Interactive and user-friendly.
* **Session Controls:** Start, end, and track sessions.
* **Crisis Alerts:** Immediate attention with prominent warnings and help.

---

## 📝 Usage Guide

1. Launch using `streamlit run app.py` or `python main.py`.
2. Begin a session and send a message.
3. The system will respond and route you to a specialist.
4. Use the sidebar (Streamlit) to manage session settings.

---

## 🚣️ Development Roadmap

* [ ] Add multilingual support
* [ ] Integrate with external mental health APIs
* [ ] Implement user authentication and privacy controls
* [ ] Expand tool library with new interventions
* [ ] Improve accessibility and mobile UI

---

## 🤝 Contributing

We welcome contributions! Feel free to fork the repository, create a feature branch, and open a pull request. For suggestions, open an issue.

---

---

**Thank you for using the Mental Health Support System!**

If you have questions or feedback, please open an issue or contact the maintainers.
