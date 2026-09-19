from smolagents import LiteLLMModel
from dotenv import load_dotenv

load_dotenv()

messages = []
model = LiteLLMModel("openai/gpt-4o", temperature=0.2)

while True:
    user_input = input("Enter a message: ")
    
    if user_input == "exit":
        break
    
    messages.append({"role": "user", "content": user_input})
    
    response = model(messages, max_tokens=500)
    assistant_message = response.content
    
    print("Assistant:", assistant_message)
    messages.append({"role": "assistant", "content": assistant_message})
