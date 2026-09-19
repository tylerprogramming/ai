#!/usr/bin/env python
import asyncio
from random import randint

from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from .crews.checklist_crew.checklist_crew import ChecklistCrew
from .crews.quote_crew.quote_crew import QuoteCrew
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class ChecklistState(BaseModel):
    checklist: str = ""
    quote: str = ""
    final_email_body: str = ""

class ChecklistFlow(Flow[ChecklistState]):

    @start()
    def generate_email_body_from_checklist(self):
        print("Generating email body from checklist")

        result = ChecklistCrew().crew().kickoff(inputs={"checklist": self.state.checklist})

        self.state.checklist = result.raw

        return result.raw
    
    @listen(generate_email_body_from_checklist)
    def generate_quote_from_email_body(self):
        print("Generating quote from email body")

        result = QuoteCrew().crew().kickoff(inputs={"checklist": self.state.checklist})

        self.state.quote = result.raw

    @listen(generate_quote_from_email_body)
    def final_email_body(self):
        print("Generating final email body")
        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"""
                    Take the checklist {self.state.checklist} and the quote {self.state.quote} and create a final email body.
                    The email body should be well formatted and again for an email.  This means in HTML.  Don't include any preamble or other text, just the body of the email.

                    Remove the subject line from the email.

                    Just personalize the email with the quote and the checklist.  Add anything else you think is important based on the checklist.  Add emojis, 
                    and again, make it beautiful.

                    The email should be well formatted in HTML.  As beautiful as you can make it.
                    """
                }
            ]
        )

        final_email_body = completion.choices[0].message.content

        # Remove ```html from the beginning and ``` from the end if they exist
        final_email_body = final_email_body.strip()
        if final_email_body.startswith("```html"):
            final_email_body = final_email_body[7:]
        if final_email_body.endswith("```"):
            final_email_body = final_email_body[:-3]
        final_email_body = final_email_body.strip()

        print(final_email_body)

        self.state.final_email_body = final_email_body

        return completion.choices[0].message.content


    @listen(generate_email_body_from_checklist)
    def save_email_body(self):
        with open("email_body.txt", "w") as f:
            f.write(self.state.checklist)

async def run_flow(checklist):
    """
    Run the flow.
    """
    checklist_flow = ChecklistFlow()

    # add to state to store for later use in flow
    checklist_flow.state.checklist = checklist

    await checklist_flow.kickoff()
    
    checklist_flow.plot("email body flow")

    print(checklist_flow.state.final_email_body)

    return checklist_flow.state.final_email_body

def main(checklist):
    return asyncio.run(run_flow(checklist))

if __name__ == "__main__":
    main()
