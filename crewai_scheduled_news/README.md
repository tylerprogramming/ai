# CrewAI Custom Tool

This package contains custom tools for use with CrewAI, specifically a custom Serper Dev search tool.

## Contents

- `crew_tool.py`: Contains the CustomSerperDevTool class for performing searches using the Serper Dev API.
- `__init__.py`: (Assumed to exist for package initialization)

## CustomSerperDevTool

The `CustomSerperDevTool` is a custom implementation of CrewAI's BaseTool, designed to perform web searches using the Serper Dev API.

### Features

- Performs web searches using Serper Dev API
- Extracts organic search results
- Returns results in a structured JSON format

### Usage

To use the CustomSerperDevTool:

1. Ensure you have the required dependencies installed:
   - crewai_tools
   - requests
   - python-dotenv

2. Set up your environment variables:
   - Create a `.env` file in your project root
   - Add your Serper Dev API key: `SERPER_API_KEY=your_api_key_here`

3. Import and use the tool in your CrewAI setup:


#### Potential Improvements

@llm
    def chat(self):
        return LLM(model="openai/chat", temperature=0.1, top_p=0.2, base_url="http://127.0.0.1:1234/v1")
        
