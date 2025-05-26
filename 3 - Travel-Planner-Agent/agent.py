from google.adk.agents import Agent



root_agent = Agent(model="gemini-2.0-flash-001",
        name="travel_agent",
        instruction = """
You are a helpful agent who assists users with their travel planning."""
,    )