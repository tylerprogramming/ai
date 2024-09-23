import os

from mem0 import MemoryClient

from autogen import ConversableAgent, UserProxyAgent
from dotenv import load_dotenv

load_dotenv()

USER_ID = "best_buy_service_bot"

agent = ConversableAgent(
    "chatbot",
    system_message="You are a helpful AI Assistant.",
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": os.environ.get("OPENAI_API_KEY")}]},
    code_execution_config=False,
    function_map=None,
    human_input_mode="NEVER",
)

memory_client = MemoryClient()

conversation = [
    {"role": "assistant", "content": "Hi, I'm Best Buy's chatbot! How can I help you?"},
    {"role": "user", "content": "I'm seeing horizontal lines on my TV."},
    {"role": "assistant", "content": "I'm sorry to hear that. Can you provide your TV model?"},
    {"role": "user", "content": "It's a Sony - 77\" Class BRAVIA XR A80K OLED 4K UHD Smart Google TV"},
    {"role": "assistant", "content": "Thank you for the information. Let's troubleshoot this issue..."}
]

memory_client.add(messages=conversation, user_id=USER_ID)
print("Conversation added to memory.")

def get_context_aware_response(question):
    relevant_memories = memory_client.search(question, user_id=USER_ID)
    context = "\n".join([m["memory"] for m in relevant_memories])

    prompt = f"""Answer the user question considering the previous interactions:
    Previous interactions:
    {context}

    Question: {question}
    """

    reply = agent.generate_reply(messages=[{"content": prompt, "role": "user"}])
    return reply


while True:
    user_input = input("You: ")
    answer = get_context_aware_response(user_input)
    print("Best Buy Chatbot:", answer)