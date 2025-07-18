from google.adk.agents import Agent
from toolbox_core import ToolboxSyncClient

toolbox = ToolboxSyncClient("http://127.0.0.1:5000")

# Load all the tools
tools = toolbox.load_toolset('my_bq_toolset')

root_agent = Agent(
    name="gcp_releasenotes_agent",
    model="gemini-2.0-flash",
    description=(
        "An inventory co-pilot to check stock levels, generate low-stock reports, and find the top-selling product of the week."
    ),
    instruction=(
        "You are an inventory specialist. Your goal is to use your tools to accurately answer user questions about product stock, low-inventory alerts, and weekly best-sellers."
    ),
    tools=tools,
)
