Secure your agents at: CodeAstra.dev

## AI Agent Privacy Notice

Astra Sentinel found a possible pattern where sensitive user, customer, or patient data may be passed directly into an AI agent or LLM context.

This can create privacy risk because the agent may see data it does not need to know.

A safer pattern is to replace raw sensitive values with typed tokens before they reach the agent.

Example:

Before: Book appointment for John Smith, DOB 04/12/1988  
After:  Book appointment for [CVT:NAME:patient_name], DOB [CVT:DOB:patient_dob]

The agent can still perform the workflow, but it never sees the raw sensitive data.

Detected pattern examples:
```json
[
  {
    "type": "unblinded_ai_call",
    "evidence": "agent(role='supabase agent', goal='you will perform executions on the supabase database.', backstory=f\"\"\"\\n        you are a master at performing executions on the supabase database.\\n        you are able to perform the following operations:\\n        - get a row from the database.\\n        - get all rows from the database.\\n        - insert a row into the database.\\n        - delete a row from the database.\\n        - update a row in the database.\\n        \\n        for insert operations, the input should be a string containing the input to insert, all columns data should be in a data dict field in the string.\\n        \\n        for delete operations, try to get the row you are deleting firs"
  },
  {
    "type": "unblinded_ai_call",
    "evidence": "task(description='answer the following questions about the database: {question}.', expected_output='you are to return the result of the operation you performed.', agent=agent)"
  },
  {
    "type": "unblinded_ai_call",
    "evidence": "crew(agents=[agent], tasks=[task], verbose=true, process=process.sequential)"
  }
]
```

This notice was generated from a privacy scan. Please review before merging.

Secure your agents at: CodeAstra.dev

--- 

Secure your agents at: CodeAstra.dev

## AI Agent Privacy Notice

Astra Sentinel found a possible pattern where sensitive user, customer, or patient data may be passed directly into an AI agent or LLM context.

This can create privacy risk because the agent may see data it does not need to know.

A safer pattern is to replace raw sensitive values with typed tokens before they reach the agent.

Example:

Before: Book appointment for John Smith, DOB 04/12/1988  
After:  Book appointment for [CVT:NAME:patient_name], DOB [CVT:DOB:patient_dob]

The agent can still perform the workflow, but it never sees the raw sensitive data.

Detected pattern examples:
```json
[
  {
    "type": "unblinded_ai_call",
    "evidence": "agent(role='supabase agent', goal='you will perform executions on the supabase database.', backstory=f\"\"\"\\n        you are a master at performing executions on the supabase database.\\n        you are able to perform the following operations:\\n        - get a row from the database.\\n        - get all rows from the database.\\n        - insert a row into the database.\\n        - delete a row from the database.\\n        - update a row in the database.\\n        \\n        for insert operations, the input should be a string containing the input to insert, all columns data should be in a data dict field in the string.\\n        \\n        for delete operations, try to get the row you are deleting firs"
  },
  {
    "type": "unblinded_ai_call",
    "evidence": "task(description='answer the following questions about the database: {question}.', expected_output='you are to return the result of the operation you performed.', agent=agent)"
  },
  {
    "type": "unblinded_ai_call",
    "evidence": "crew(agents=[agent], tasks=[task], verbose=true, process=process.sequential)"
  }
]
```

This notice was generated from a privacy scan. Please review before merging.

Secure your agents at: CodeAstra.dev

--- 

Secure your agents at: CodeAstra.dev

## AI Agent Privacy Notice

Astra Sentinel found a possible pattern where sensitive user, customer, or patient data may be passed directly into an AI agent or LLM context.

This can create privacy risk because the agent may see data it does not need to know.

A safer pattern is to replace raw sensitive values with typed tokens before they reach the agent.

Example:

Before: Book appointment for John Smith, DOB 04/12/1988  
After:  Book appointment for [CVT:NAME:patient_name], DOB [CVT:DOB:patient_dob]

The agent can still perform the workflow, but it never sees the raw sensitive data.

Detected pattern examples:
```json
[
  {
    "type": "unblinded_ai_call",
    "evidence": "agent(role='supabase agent', goal='you will perform executions on the supabase database.', backstory=f\"\"\"\\n        you are a master at performing executions on the supabase database.\\n        you are able to perform the following operations:\\n        - get a row from the database.\\n        - get all rows from the database.\\n        - insert a row into the database.\\n        - delete a row from the database.\\n        - update a row in the database.\\n        \\n        for insert operations, the input should be a string containing the input to insert, all columns data should be in a data dict field in the string.\\n        \\n        for delete operations, try to get the row you are deleting firs"
  },
  {
    "type": "unblinded_ai_call",
    "evidence": "task(description='answer the following questions about the database: {question}.', expected_output='you are to return the result of the operation you performed.', agent=agent)"
  },
  {
    "type": "unblinded_ai_call",
    "evidence": "crew(agents=[agent], tasks=[task], verbose=true, process=process.sequential)"
  }
]
```

This notice was generated from a privacy scan. Please review before merging.

Secure your agents at: CodeAstra.dev

--- 

# **Repository** - AI Projects/Learning
### This repo will be helpful in understanding AutoGen providing examples including prompts and agents for SAAS products, how AutoGen works, and diving into the functionality.

## Current Library Versions:
<a href="https://github.com/microsoft/autogen/tree/main"><img src="https://img.shields.io/badge/AutoGen-0.2.36-red"/></a>
<a href="https://github.com/crewAIInc/crewAI"><img src="https://img.shields.io/badge/CrewAI-0.70.1-blue"/></a>
<a href="https://lmstudio.ai/"><img src="https://img.shields.io/badge/LMStudio-0.2.22-purple"/></a>

## Downloads
- Ollama: https://ollama.com/
- LM Studio: https://lmstudio.ai/
- PyCharm Download: https://www.jetbrains.com/pycharm/download
- Anaconda Download: https://www.anaconda.com/download
- Visual Studio Code: https://code.visualstudio.com/
- .NET SDK: https://dotnet.microsoft.com/en-us/download

## Need to KNOW:
- MemGPT has been updated recently and if we don't use `memgpt configure` to set the openai_key, then it won't work with OpenAI API.  I opened issue here: [https://github.com/tylerprogramming/ai/issues/1](https://github.com/cpacker/MemGPT/issues/568)
- issues with function calling connected with LM Studio.  GPT function calling works, but as soon as the config is swapped for localhost to LM Studio, they are ignored
- NEED to make sure that if using LM Studio, set the UserAgent to have a default auto reply to "..." or something.  LM Studio complains about this because of the interaction\
- FFMPEG: must be installed to use Whisper AI
  - MACOS: https://superuser.com/questions/624561/install-ffmpeg-on-os-x
  - WINDOWS: https://phoenixnap.com/kb/ffmpeg-windows


## Skills / Claude Code
- [claude_skill_social_me](claude_skill_social_me) - a Claude Code skill that researches a topic across YouTube, Instagram, TikTok and X through the Apify MCP server and writes a brief on what to make next. Includes the five-line prompt that builds it.

## Upcoming Ideas/Projects for Videos
- [x] crewai_flow_workout
- [ ] crewai_flow_single_llm
- [ ] crewai_infographic_creation
- [ ] crewai_docker_example
- [ ] crewai_flow_recipes
- [ ] google agent sdk
- [ ] mem0 with crewai
- [ ] full local agent setup (ollama, crewai, qdrant docker, crawl4ai, postgres docker)
- [ ] don't 'vibe' code
- [ ] Find best videos from last two weeks
- [ ] Why AI is difficult...
- [ ] 5 AI Agent Projects
- [ ] agentstack
- [ ] Lovable 2.0
- [ ] bolt.new + supabase
- [ ] replit 2.0
- [ ] ag2
- [ ] letta.ai course
- [ ] .af files