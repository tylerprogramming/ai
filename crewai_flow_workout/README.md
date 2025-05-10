# CrewAI Workout Flow

A sophisticated AI-powered workout planning system that leverages CrewAI for orchestrating multiple AI agents to create, research, and deliver personalized workout plans.

## 🌟 Features

- Automated workout research and planning
- Integration with Google Drive for document storage
- CSV and Document format workout plans
- Slack notifications for workout plans
- Intelligent flow management using CrewAI
- Research and summarization capabilities
- It works!

## 🏗️ Architecture

The project uses a flow-based architecture powered by CrewAI, with multiple specialized agents working together:

1. **Google Drive Agent**: Manages folder creation and file storage
2. **Research Crew**: Conducts workout research
3. **Summary Crew**: Summarizes workout information
4. **Workout Plan Agent**: Creates detailed workout plans in multiple formats
5. **Slack Agent**: Handles communication through Slack

## 🔧 Technical Stack

- **Core Framework**: CrewAI
- **AI Model**: GPT-4
- **Integrations**:
  - Google Drive API
  - Slack API
  - Composio Tools
- **Data Formats**: CSV, DOCX
- **State Management**: Pydantic models

## 📋 Prerequisites

- Python 3.x
- Composio API Key
- Google Drive API credentials
- Slack API credentials

## 🔑 Environment Variables

Create a `.env` file with the following:

```env
COMPOSIO_API_KEY=your_composio_api_key
```

## 📦 Dependencies

```python
crewai
composio_crewai
pydantic
python-dotenv
```

## 🚀 Flow Structure

The workflow follows this sequence:

1. **Drive Folder Setup** (`create_or_retrieve_drive_folder`):
   - Creates or finds a Google Drive folder for workout plans

2. **Workout Research** (`research_workouts`):
   - Conducts research on workouts using the Research Crew

3. **Workout Summarization** (`summarize_workouts`):
   - Processes and summarizes workout information

4. **Plan Creation** (Parallel processes):
   - `create_doc_workout_plan`: Creates a human-readable workout document
   - `create_csv_workout_plan`: Generates a detailed CSV format plan with days and reps

5. **Storage and Communication**:
   - `save_workout_plan`: Saves both formats to Google Drive
   - `send_slack_message`: Notifies users via Slack

## 💾 State Management

The system uses Pydantic models for state management:

- `WorkOutState`: Main state container
- `WorkOutResearch`: Research data structure
- `DriveFolder`: Google Drive folder information

## 🏃‍♂️ Running the Project

```bash
python src/work_out_flow/main.py
```

## 📊 Output

The system generates two types of workout plans:
1. A human-readable document (DOCX)
2. A detailed CSV file with:
   - Days of the week
   - Exercise specifications
   - Rep counts
   - Detailed workout information

Both files are automatically saved to Google Drive and a notification is sent to Slack.

## 🔍 Monitoring

The system provides verbose output for all agent activities, making it easy to monitor the workflow progress and debug issues.