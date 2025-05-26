import os
import time
import pickle
from dotenv import load_dotenv
from PIL import Image

# ADK and Gemini imports
from google.adk.agents import Agent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import google.generativeai as genai

# Load .env if present
load_dotenv()

# Configuration
MODEL = os.getenv("MODEL", "gemini-2.5-flash-preview-04-17")
APP_NAME = "invoice_extractor_agent"

# Configure Gemini
genai.configure()

# ADK services
session_service = InMemorySessionService()
artifact_service = InMemoryArtifactService()

# --- Tool Function ---
def extract_invoice_details(image_path: str) -> str:
    """
    Uses Gemini Pro Vision to extract invoice details from an image.
    Returns a structured string summary.
    """
    try:
        image = Image.open(image_path)

        prompt = """
You are an intelligent invoice parser.
Please extract the following fields from the provided invoice image:
- Invoice Number
- Invoice Date
- Vendor Name
- Line Items (Item, Quantity, Unit Price, Total Price)
- Subtotal
- Taxes (if any)
- Grand Total

Respond in structured JSON format.
"""

        model = genai.GenerativeModel(MODEL)
        response = model.generate_content([prompt, image])

        return response.text

    except Exception as e:
        return f"❌ Error processing image: {e}"

# --- Agent Definition ---
agent_instruction = """
You are a helpful invoice assistant.
You can extract key invoice details from images using the 'extract_invoice_details' tool.
When a user provides an image file path (e.g., 'sample_invoice.jpg'), extract and return structured invoice data.
If the path is invalid or unreadable, return a helpful error.
"""

root_agent = Agent(
    model=MODEL,
    name="invoice_agent",
    description="Extracts structured invoice data from image files using Gemini.",
    instruction=agent_instruction,
    tools=[extract_invoice_details],
    generate_content_config=types.GenerateContentConfig(temperature=0.2),
)

# --- Runner Function ---
def send_query_to_agent(agent, query: str):
    session = session_service.create_session(app_name=APP_NAME, user_id="user")
    content = types.Content(role="user", parts=[types.Part(text=query)])

    runner = Runner(
        app_name=APP_NAME,
        agent=agent,
        artifact_service=artifact_service,
        session_service=session_service,
    )

    events = runner.run(user_id="user", session_id=session.id, new_message=content)

    for event in events:
        if event.is_final_response() and event.content:
            print("\n🧾 Final Extracted Invoice Details:")
            print(event.content.parts[0].text)

# --- CLI Interface ---
if __name__ == "__main__":
    print("💬 Type a command like: 'Extract details from invoice.jpg'")
    print("📂 Make sure the image exists in your working directory.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        if not user_input.strip():
            continue
        send_query_to_agent(root_agent, user_input)
