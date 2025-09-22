# Google Calendar AI Agent with Gemini and ADK

![Agent Capabilities](screenshots/screenshot_capabilities.png) <!-- Replace with your actual screenshot -->

## Overview

This project showcases a sophisticated AI agent designed to manage your Google Calendar entirely through natural language. Built using Google's Agent Development Kit (ADK) and powered by the Gemini 2.0 Flash model, this agent provides an intuitive, conversational interface for scheduling, updating, deleting, searching events, and even suggesting optimal meeting times. It intelligently handles complex natural language date/time expressions, automatically detects and uses your local timezone, and gracefully manages optional event details.

This agent is a "one-stop" solution aiming to simplify personal calendar management, demonstrating the power of combining advanced LLMs with robust custom tooling and external APIs.

## Features

*   🗣️ **Natural Language Understanding:** Parses diverse date/time phrases like "next Friday at 11 AM," "tomorrow morning," "in two hours," and "for 45 minutes."
*   🌍 **Automatic Timezone Awareness:** Automatically detects your local timezone (e.g., Asia/Kolkata) for interpreting inputs and displaying outputs, converting to UTC for Google Calendar API calls.
*   ➕ **Event Creation:** Schedule new events with summary, start/end times, optional location, description, recurrence, and attendees.
*   🔄 **Event Updates:** Modify existing events by ID, changing any detail from time to description.
*   🗑️ **Event Deletion:** Cancel or remove events from your calendar.
*   🔍 **Event Search & Listing:** Find specific events by keyword or list upcoming events, displayed clearly in your local timezone.
*   🗓️ **Recurrence Handling:** Create recurring events from natural language (e.g., "every Tuesday for 5 weeks").
*   👥 **Attendee Management:** Invite participants to your events.
*   💡 **Meeting Time Suggestions:** Proactively suggests available time slots for meetings based on your calendar's free/busy status and preferred time windows.
*   ✅ **Robustness:** Built to handle ambiguous inputs, gracefully manage optional parameters, and recover from common API-related issues.

## Prerequisites

Before you begin, ensure you have the following:

1.  **Python 3.9+** installed on your system.
2.  A **Google Cloud Project**. If you don't have one, create it [here](https://console.cloud.google.com/).
3.  The **Google Calendar API enabled** in your Google Cloud Project.
    *   Navigate to **APIs & Services > Library** and search for "Google Calendar API." Enable it.
4.  **OAuth 2.0 Client ID Credentials:**
    *   In your Google Cloud Project, go to **APIs & Services > Credentials**.
    *   Click **+ CREATE CREDENTIALS** and select **OAuth client ID**.
    *   For the Application type, choose **Desktop app**. Give it a descriptive name (e.g., `CalendarAgent`).
    *   Click **CREATE** and then **DOWNLOAD JSON**. Save this file as `credentials.json` in the root directory of this project.

## Setup Instructions

Follow these steps to get your Google Calendar Agent up and running:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/my-calendar-agent.git # REPLACE WITH YOUR REPO URL
    cd my-calendar-agent
    ```

2.  **Create and Activate a Python Virtual Environment:**
    It's good practice to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows:
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    Install all required Python packages using the `requirements.txt` file.
    *(You can generate this by running `pip freeze > requirements.txt` in your activated virtual environment after installing all listed packages.)*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Place `credentials.json`:**
    Ensure the `credentials.json` file you downloaded from Google Cloud is placed directly in the `my-calendar-agent/` directory. **Remember: Do NOT commit `credentials.json` to your public repository! It is already in `.gitignore`.**

## How to Run

1.  **Start the Agent:**
    ```bash
    python main.py
    ```

2.  **First-time Authentication:**
    *   The first time you run the agent, a browser window will open, prompting you to log in with your Google account and grant permissions to access your calendar.
    *   After successful authentication, a `token.json` file will be created in your project directory. This file securely stores your refresh tokens, so you won't need to re-authenticate on subsequent runs unless the token expires or is manually deleted. **(`token.json` is also in `.gitignore`)**

3.  **Interact with the Agent:**
    Once authenticated, you'll see a prompt:
    ```
    Google Calendar Agent Ready! Type 'exit' to quit.
    You:
    ```
    You can now start conversing with your agent!

## Usage Examples (Demonstrations)

Here are a few examples of how you can interact with the agent, showcasing its natural language understanding and tool integration. Remember to capture screenshots of your own interactions to replace the placeholders!

---

### **1. Discovering Agent Capabilities**

Ask the agent what it can do to get a quick overview of its features.
