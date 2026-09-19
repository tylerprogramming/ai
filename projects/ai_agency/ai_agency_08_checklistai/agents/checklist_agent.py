from pydantic import BaseModel
from openai import OpenAI

class MyChecklist(BaseModel):
    title: str
    items: list[str]

class ChecklistAgent:
    def __init__(self, client: OpenAI):
        self.client = client

    def generate_checklist(self, prompt: str) -> MyChecklist:
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "Extract the checklist information."},
                {"role": "user", "content": f"Create a checklist for: {prompt}. Give a fun title for the description of the checklist they provided."},
            ],
            response_format=MyChecklist,
        )
        return completion.choices[0].message.parsed
