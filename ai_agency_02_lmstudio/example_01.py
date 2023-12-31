from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

completion = client.chat.completions.create(
    model="local-model",
    messages=[
        {"role": "system", "content": "You are a fitness expert."},
        {"role": "user", "content": "I want you to create a single day workout for arms."}
    ],
    temperature=0.7,
)

print(completion.choices[0].message.content)
