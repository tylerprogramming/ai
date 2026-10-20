from smolagents import LiteLLMModel
from dotenv import load_dotenv

load_dotenv()

messages = []
model = LiteLLMModel("openai/gpt-5.4-mini")  # gpt-5 models only support the default temperature

while True:
    user_input = input("Enter a message: ")
    
    if user_input == "exit":
        break
    
    messages.append({"role": "user", "content": user_input})
    
    response = model(messages, max_completion_tokens=500)  # gpt-5 models use max_completion_tokens
    assistant_message = response.content
    
    print("Assistant:", assistant_message)
    messages.append({"role": "assistant", "content": assistant_message})
