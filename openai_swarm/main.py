from swarm import Swarm, Agent

client = Swarm()

def transfer_to_agent_b():
    return agent_b


agent_a = Agent(
    name="Agent A",
    instructions="You are a helpful agent.",
    functions=[transfer_to_agent_b],
)

agent_b = Agent(
    name="Agent B",
    instructions="Only speak in Haikus.",
)

response = client.run(
    agent=agent_a,
    messages=[{"role": "user", "content": "I want to talk to agent B."}],
    stream=True,
)

# for streaming
message = ""
for chunk in response:
    # Check if content exists and is not None
    if chunk.get('content'):
        message += chunk['content']
        # If you want to see each piece as it comes in:
        print(chunk['content'], end='')

# for non-streaming
# print(response.messages[-1]["content"])