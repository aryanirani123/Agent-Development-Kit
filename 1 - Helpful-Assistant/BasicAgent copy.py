import os
import time

# Import libraries from the Agent Framework
from google.adk.agents import Agent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from dotenv import load_dotenv
load_dotenv()

# Get the model ID from the environment variable
MODEL = os.getenv("MODEL", "gemini-2.0-flash-001") # The model ID for the agent
AGENT_APP_NAME = 'agent_basic'

# Create InMemory services for session and artifact management
session_service = InMemorySessionService()
artifact_service = InMemoryArtifactService()

def send_query_to_agent(agent, query):
    """Sends a query to the specified agent and prints the response.

    Args:
        agent: The agent to send the query to.
        query: The query to send to the agent.

    Returns:
        A tuple containing the elapsed time (in milliseconds) and the final response from the agent.
    """

    # Create a new session - if you want to keep the history of interaction you need to move the 
    # creation of the session outside of this function. Here we create a new session per query
    session = session_service.create_session(app_name=AGENT_APP_NAME,
                                             user_id='user',)
    # Create a content object representing the user's query
    print('\nUser Query: ', query)
    content = types.Content(role='user', parts=[types.Part(text=query)])

    # Start a timer to measure the response time
    start_time = time.time()

    # Create a runner object to manage the interaction with the agent
    runner = Runner(app_name=AGENT_APP_NAME, agent=agent, artifact_service=artifact_service, session_service=session_service)

    # Run the interaction with the agent and get a stream of events
    events = runner.run(user_id='user', session_id=session.id, new_message=content)

    final_response = None
    elapsed_time_ms = 0.0

    # Loop through the events returned by the runner
    for _, event in enumerate(events):

        is_final_response = event.is_final_response()

        if not event.content:
             continue

        if is_final_response:
            end_time = time.time()
            elapsed_time_ms = round((end_time - start_time) * 1000, 3)

            print("-----------------------------")
            print('>>> Inside final response <<<')
            print("-----------------------------")
            final_response = event.content.parts[0].text # Get the final response from the agent
            print(f'Agent: {event.author}')
            print(f'Response time: {elapsed_time_ms} ms\n')
            print(f'Final Response:\n{final_response}')
            print("----------------------------------------------------------\n")

    return elapsed_time_ms, final_response

if __name__ == '__main__':

    # Create a basic agent with instructions amd greeting only
    basic_agent = Agent(model=MODEL,
        name="agent_basic",
description = """
This is a basic conversational agent built using the Google Agent Framework. It is designed to answer questions about a developer talk on Agent Development Kits (ADK), presented by Aryan Irani, a Google Developer Expert. The agent demonstrates how simple instruction-based agents can provide helpful responses without tools or memory. It serves as an introductory example to the ADK system.
""",
        instruction = """
You are a helpful assistant designed to answer questions about a talk on Agent Development Kits (ADK), delivered by Aryan Irani, a Google Developer Expert (GDE).

Your job is to provide accurate answers about the talk's content, agenda, and speaker. You were built using the Google Agent Framework and this demo shows how simple agents can be created using the ADK.

The session includes:
- An introduction to the evolution of AI and the leap into agentic AI
- What is an AI agent?
- Introduction to ADK (Agent Development Kit)
- Foundations of ADK: LLM core, tools and functions, memory, and runner
- Demo 1: A simple agent that answers questions about this session
- Demo 2: An Expense Logger agent
- Demo 3: A To-do List agent integrated with Google Tasks
- Advanced topics like multi-agent systems, tool orchestration, and memory strategies
- Conclusion with resources and next steps for developers

When someone asks:
- "Tell me about this talk" → Summarize the talk as described above
- "Who is giving this talk?" or "Who is Aryan Irani?" → Say that Aryan Irani is a Google Developer Expert leading this session
- "What will I learn today?" → Briefly list the major sections
- "What is ADK?" → Say it's the Agent Development Kit by Google for building AI agents
- "What demos are included?" → Mention the basic agent, expense logger, and task list manager

Keep your answers short and clear. Stay on topic. Do not hallucinate or make up topics not listed above. If a question is unrelated, kindly say, "I'm here to answer questions about today's session only."
"""
,
        generate_content_config=types.GenerateContentConfig(temperature=0.2),
    )

    # Send a single query to the agent
    send_query_to_agent(basic_agent, "Are there going to be any demos?")

    # Example of sending multiple queries to the agent (commented out)
    # queries = [
    #     "Hi, I am Tom",
    #     "Could you let me know what you could do for me?",
    #     "How were you built?",
    # ]

    # for query in queries:
    #     send_query_to_agent(basic_agent, query)


