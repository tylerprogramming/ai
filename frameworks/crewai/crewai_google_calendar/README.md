# CrewAI Google Calendar Project

The `crewai_google_calendar` project is designed to automate interactions with Google Calendar and Gmail using the CrewAI framework. It leverages the Composio toolset to perform actions such as finding free slots, creating events, and sending emails.

## Key Components

1. **Main Script (`main.py`)**:
   - **Purpose**: The main script serves as the entry point for running the GoogleCrew. It sets up the input query for creating a daily standup meeting and checks for available slots in the calendar.
   - **Functionality**: 
     - Defines a `run()` function that initializes the `GoogleCrew` and executes it with specified inputs.
     - The input query specifies the creation of a daily standup meeting from Monday to Thursday, checking for availability, and sending an email notification.
     - Handles exceptions and prints the result of the crew execution.

2. **Crew Definition (`crew.py`)**:
   - **Purpose**: Defines the `GoogleCrew` class, which orchestrates the interaction with Google Calendar and Gmail.
   - **Components**:
     - **Agents**: 
       - `google_agent`: Configured to interact with Google Calendar using tools for finding events, free slots, creating, deleting, and updating events.
       - `gmail_agent`: Configured to send emails using Gmail.
     - **Tasks**:
       - `google_task`: Manages tasks related to Google Calendar operations.
       - `gmail_task`: Manages tasks related to sending emails.
     - **Crew**: 
       - Combines agents and tasks into a sequential process for execution.
       - Uses decorators to automatically create agents and tasks from configuration files.

3. **Configuration**:
   - **Environment Variables**: Loaded using `dotenv` to manage API keys and other sensitive information.
   - **Composio Toolset**: Utilized to access Google Calendar and Gmail actions through predefined tools.

## Usage

To run the project, execute the `main.py` script. It will:
- Create a daily standup meeting in Google Calendar if slots are available.
- Send an email notification using Gmail.

## Setup

1. **Environment Setup**:
   - Ensure that the necessary environment variables are set in a `.env` file.
   - Install required dependencies as specified in the `pyproject.toml`.

2. **Execution**:
   - Run the `main.py` script to initiate the GoogleCrew process.

## Conclusion

This project automates the scheduling of meetings and email notifications, providing a seamless integration with Google services through the CrewAI framework. It demonstrates the use of agents and tasks to manage complex workflows efficiently.
