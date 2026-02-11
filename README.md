MindCrew Companion:

MindCrew Companion is a specialized AI-driven wellness application designed to provide empathetic support and motivational guidance. This document outlines the technical architecture and the functional modules that power the platform.

Technical Architecture
The project is built using a modern Python stack designed for rapid deployment and high interactivity.

Core Technologies
Frontend Framework Streamlit was chosen for its ability to handle state management and reactive UI components with zero JavaScript overhead.

Intelligence Engine Google Gemini API utilizes the gemini-1.5-flash model for high-speed, low-latency natural language processing.

Styling Custom CSS Injection was used to implement a Glassmorphic UI including blur effects and semi-transparent layers over a dynamic CSS gradient background.

Functional Modules
1. Navigation & State Controller
This module serves as the app's "router." Since Streamlit typically runs as a single-page script, this controller uses session state variables to track which screen the user is on. It manages the transition between the Dashboard, the Mood Advisor, and the Chat Support without refreshing the entire application or losing temporary data.

2. Mood Advisor Module
This module is designed for quick, targeted wellness interventions. It captures user input regarding their current emotional state and sends a structured prompt to the Gemini AI. The AI is instructed to return two specific components: a supportive empathetic statement and a practical wellness tip. This ensures the user receives actionable advice immediately.

3. Empathetic Chat Support Module
The Chat module handles multi-turn conversations. It maintains a "message history" list in the session state so the AI can remember what the user said previously. It formats the UI using distinct "user" and "assistant" chat bubbles to simulate a real-time messaging experience, providing a safe space for deeper expression.

4. AI Engine & Discovery Module
This is the backend logic that connects to Google Generative AI. It includes a discovery script that automatically scans for the most efficient "Flash" model available in the user's API tier. By automating model selection, the module prevents the app from breaking if specific model versions are updated or retired by Google.

Key Code Implementations
Dynamic AI Support
The get_ai_response function acts as the central brain, handling error catching and model selection:

Python
def get_ai_response(prompt):
    # Filters models to find the most efficient 'flash' variant
    available_models = [m.name for m in genai.list_models()]
    target_model = next((m for m in available_models if "flash" in m.lower()), available_models[0])
    # ... generation logic ...
Deployment Process
Dependency Mapping All libraries are frozen into requirements.txt for environment parity.

Secrets Configuration API keys are injected via the hosting provider's Secrets Management rather than being stored in the code.

Continuous Integration Connected via GitHub to Streamlit Community Cloud for automatic deployments upon every git push.
