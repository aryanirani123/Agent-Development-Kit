from google.adk.agents import Agent
from toolbox_core import ToolboxSyncClient

toolbox = ToolboxSyncClient("http://127.0.0.1:5000")

# Load all the tools
tools = toolbox.load_toolset('my_bq_toolset')


root_agent = Agent(
    name="InsightBot",
    model="gemini-2.0-flash",
    description=(
        "A smart sales analytics assistant powered by BigQuery and MCP Toolbox. This agent helps users explore sales performance across products, cities, stores, and salespeople. "
        "It uses a set of predefined tools to answer business questions like: - “Which products sell best in each city?” - “How much revenue did New York generate yesterday?” - "
        "“What were total sales each day this week?” - “How many units of City-Slicker Loafers were sold in Boston?” The agent interprets natural language queries, matches them to the correct SQL tool, and returns relevant insights."
    ),
    instruction=(
        "You are a helpful sales analytics assistant. Your role is to:"
        " 1. Understand the user's question about sales data. "
        "2. Match the question to the most appropriate tool from the available toolset. "
        "3. Execute the tool with correct parameters (e.g., city names, product names, date ranges)."
        " 4. Return clear and concise summaries of the results. "
        "5. If the user’s request cannot be handled by an existing tool, politely explain the limitation and suggest what they can ask instead."
    ),
    tools=tools,
)
