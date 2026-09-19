# Personalized Workout Plan Generator with crewAI

This project is a simple, interactive AI workflow that generates a personalized daily workout plan using a single LLM (Large Language Model) via the [crewAI](https://crewai.com) framework. The user provides their daily routine and workout habits, and the system creates a tailored workout plan, saving it as a markdown file.

## How It Works

- **User Input:** The program prompts the user for their wake-up time, bedtime, workout frequency, and running frequency.
- **Prompt Construction:** These inputs are used to build a prompt for the LLM, asking it to generate a daily workout plan.
- **LLM Call:** The system uses Google Gemini (or can be configured for OpenAI GPT-4o) to generate the workout plan, expecting a structured response.
- **Output:** The generated plan is saved to a markdown file (`workout_plan_google.md` by default).

## Project Structure

```
single_llm/
  ├── pyproject.toml         # Project metadata and dependencies
  ├── README.md              # (This file)
  └── src/
      └── single_llm/
          ├── main.py       # Main workflow logic
          ├── prompts.py    # Prompt construction for the LLM
          └── __init__.py
```

## Key Files

- **main.py:**  
  - Defines the flow using crewAI's `Flow` class.
  - Handles user input, LLM interaction, and saving the output.
  - Uses environment variables (e.g., `GEMINI_API_KEY`) for LLM access.

- **prompts.py:**  
  - Contains the function to build the prompt for the LLM based on user input.

## Setup

1. **Install Python**  
   Requires Python >=3.10 and <3.13.

2. **Install Dependencies**  
   Use pip or your preferred tool:
   ```bash
   pip install crewai[tools]>=0.114.0,<1.0.0
   ```

3. **Set Environment Variables**  
   Create a `.env` file in the project root and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_google_gemini_api_key
   ```

## Running the Project

From the `single_llm` directory, run:

```bash
python src/single_llm/main.py
```

You will be prompted for your daily routine details. The generated workout plan will be saved as `workout_plan_google.md`.

## Customization

- To use a different LLM (like OpenAI GPT-4o), modify the `main.py` to instantiate the `LLM` class with your desired model and API key.
- You can change the output file path by editing the `output_path` in `SingleLLMState`.