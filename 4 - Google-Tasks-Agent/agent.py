import os
import pickle # For storing token
from google.adk.agents import Agent
from google.genai import types
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


MODEL = "gemini-2.0-flash-001" # Using a more recent model
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/tasks']
TOKEN_PICKLE_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json' # Make sure this file is in the same directory

# --- Google Tasks API Service ---
def get_tasks_service():
    """Shows basic usage of the Google Tasks API.
    Returns an authenticated Google Tasks API service object.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"'{CREDENTIALS_FILE}' not found. "
                    "Please download it from Google Cloud Console and place it in the current directory."
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            # Run local server for web-based OAuth, or print URL for console-based
            # For a truly headless environment, you might need a different flow or pre-authorized service account.
            # This setup is typical for desktop/CLI apps run by a user.
            creds = flow.run_local_server(port=0) # Use run_console() if no browser access
        # Save the credentials for the next run
        with open(TOKEN_PICKLE_FILE, 'wb') as token:
            pickle.dump(creds, token)

    try:
        service = build('tasks', 'v1', credentials=creds)
        return service
    except Exception as e:
        print(f"An error occurred building the service: {e}")
        # Potentially re-raise or handle more gracefully
        # If token.pickle is corrupted, deleting it might help
        if os.path.exists(TOKEN_PICKLE_FILE):
            print(f"Try deleting '{TOKEN_PICKLE_FILE}' and running again.")
        raise

# --- Tool Functions (modified for Google Tasks API) ---

# Cache for task list and IDs to avoid multiple API calls if agent needs it.
# This is a simple in-memory cache for the duration of one user query processing.
_task_list_cache = None
_task_id_map_cache = None # Maps simple numbers (1, 2, 3...) to Google Task IDs for user convenience




def _fetch_and_cache_tasks(service):
    """Helper to fetch tasks and populate caches."""
    global _task_list_cache, _task_id_map_cache
    _task_list_cache = []
    _task_id_map_cache = {}
    try:
        # Using '@default' for the primary task list
        results = service.tasks().list(tasklist='@default', showCompleted=False, showHidden=False, maxResults=100).execute()
        items = results.get('items', [])
        if items:
            for i, task_item in enumerate(items):
                # Only add non-completed tasks to the simplified list for the agent
                if task_item.get('status') != 'completed':
                    _task_list_cache.append({
                        'id': task_item['id'], # Google's Task ID
                        'title': task_item['title'],
                        'notes': task_item.get('notes', '')
                    })
                    _task_id_map_cache[i + 1] = task_item['id'] # Map 1, 2, 3... to Google ID
        return items # Return raw items as well if needed elsewhere
    except HttpError as err:
        print(f"An API error occurred while fetching tasks: {err}")
        return [] # Return empty on error to prevent crash

def list_tasks() -> str:
    """Lists all current, non-completed tasks from Google Tasks with a simple numeric ID for user interaction."""
    global _task_list_cache, _task_id_map_cache
    service = get_tasks_service()
    _fetch_and_cache_tasks(service) # Refresh cache

    if not _task_list_cache:
        return "Your Google Tasks list is empty or all tasks are completed."

    output = "Your Google To-Do List (pending tasks):\n"
    for i, task in enumerate(_task_list_cache):
        output += f"{i + 1}. {task['title']}\n" # User sees 1, 2, 3...
    output += "\nUse the number to refer to tasks for completion."
    return output.strip()

def add_task(description: str) -> str:
    """Adds a new task to the default Google Tasks list."""
    global _task_list_cache # Invalidate cache
    service = get_tasks_service()
    task_body = {
        'title': description,
        # 'notes': 'Optional notes here' # You can extend this
    }
    try:
        created_task = service.tasks().insert(tasklist='@default', body=task_body).execute()
        _task_list_cache = None # Invalidate cache as list has changed
        return f"Task '{description}' added to Google Tasks with ID {created_task['id']}."
    except HttpError as err:
        print(f"An API error occurred while adding task: {err}")
        return f"Error adding task '{description}' to Google Tasks. Please check logs."

def complete_task(task_number: int) -> str:
    """
    Marks a task as complete in Google Tasks given its simple numeric ID from the list_tasks command.
    """
    global _task_list_cache, _task_id_map_cache
    service = get_tasks_service()

    # If cache is empty (e.g., direct call without listing), try to populate it
    if not _task_id_map_cache:
        _fetch_and_cache_tasks(service)
        if not _task_id_map_cache: # Still empty after fetch
            return "Could not find tasks to complete. Please list tasks first."

    google_task_id = _task_id_map_cache.get(task_number)

    if not google_task_id:
        return f"Error: Task number {task_number} not found in the current list. Please use 'list_tasks' to see available task numbers."

    try:
        # Fetch the task to get its current details (like title)
        task_to_complete = service.tasks().get(tasklist='@default', task=google_task_id).execute()
        task_title = task_to_complete.get('title', 'Unknown Task')

        if task_to_complete.get('status') == 'completed':
            return f"Task '{task_title}' (ID: {google_task_id}) is already completed."

        # Update task status to 'completed'
        # The body for update requires the ID and the fields to be updated.
        # For completing a task, you primarily set 'status' to 'completed'.
        # You also need to provide the 'id' of the task in the body.
        updated_task_body = {
            'id': google_task_id,
            'status': 'completed'
        }
        service.tasks().update(tasklist='@default', task=google_task_id, body=updated_task_body).execute()
        _task_list_cache = None # Invalidate cache
        _task_id_map_cache = None
        return f"Task '{task_title}' (ID: {google_task_id}) has been marked as completed in Google Tasks."
    except HttpError as err:
        if err.resp.status == 404:
            return f"Error: Task with Google ID {google_task_id} (number {task_number}) not found in Google Tasks."
        print(f"An API error occurred while completing task: {err}")
        return f"Error completing task number {task_number}. Please check logs."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return f"An unexpected error occurred while completing task number {task_number}."


# --- Agent Definition ---
agent_todo_instruction_text = """
You are a helpful to-do list assistant that interacts with Google Tasks.
You have tools to add, list, and complete tasks.
- To add a task, use the 'add_task' tool with the task description.
- To see your tasks, use the 'list_tasks' tool. This will show pending tasks with a number.
- To complete a task, use the 'complete_task' tool with the task's number (e.g., if 'list_tasks' shows "1. Buy milk", use 1 for 'task_number').
If the user refers to a task by description for completion, first list the tasks to help them find the correct number, then ask for the number.
Always confirm actions taken.
When listing tasks, inform the user that the numbers provided are for use with the 'complete_task' tool.
If 'complete_task' is called with a description, tell the user you need the task number from the list and suggest they list tasks first.
"""

root_agent = Agent(
    model=MODEL,
    name="agent_todo_google_tasks",
    description="A conversational agent to manage a to-do list using Google Tasks."+agent_todo_instruction_text,
    generate_content_config=types.GenerateContentConfig(temperature=0.2),
    tools=[list_tasks, add_task, complete_task],
)