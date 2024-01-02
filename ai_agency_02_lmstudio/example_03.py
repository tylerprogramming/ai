from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")


def get_completion(prompt, model="local model", temperature=0.7):
    formatted_prompt = f"Hello! Please give me 3 words that rhyme with {prompt}"
    messages = [{"role": "user", "content": formatted_prompt}]
    print(f'\nYour prompt: {formatted_prompt}\n')

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )

    return completion.choices[0].message


prompt = input("Hello! Please give me 3 words that rhyme with... ")
response = get_completion(prompt)
print(f"LLM response: {response}")
