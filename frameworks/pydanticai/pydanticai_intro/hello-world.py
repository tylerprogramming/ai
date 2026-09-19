from pydantic_ai import Agent

agent = Agent(  
    'openai:gpt-4o',
    system_prompt='Be concise, reply with one sentence.',  
)

result = agent.run_sync('Where does "hello world" come from?')  
print(result.data)