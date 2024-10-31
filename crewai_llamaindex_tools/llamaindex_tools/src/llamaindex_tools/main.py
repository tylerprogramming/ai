#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start

from crews.wikipedia_crew.wikipedia_crew import WikipediaCrew
from crews.math_crew.crew import MathCrew

class WikipediaState(BaseModel):
    topic: str = ""
    query_str: str = ""

class WikipediaFlow(Flow[WikipediaState]):
    @start()
    def generate_topic(self):
        print("Generating topic")
        self.state.topic = "San Fransisco"

    @listen(generate_topic)
    def generate_wikipedia_query(self):
        print("Generating wikipedia query")
        self.state.query_str = "What's the arts and culture scene in San Fransisco?"

    @listen(generate_wikipedia_query)
    def generate_wikipedia_result(self):
        print("Generating wikipedia result")
        result = (
            WikipediaCrew()
            .crew()
            .kickoff(inputs={"topic": self.state.topic, "query_str": self.state.query_str})
        )

        print("Wikipedia query generated", result.raw)
        self.state.query_str = result.raw

    @listen(generate_wikipedia_result)
    def save_wikipedia_result(self):
        print("Saving wikipedia result")
        with open("wikipedia_result.txt", "w") as f:
            f.write(self.state.query_str)

    @listen(generate_wikipedia_result)
    def generate_math_result(self):
        print("Generating math result")
        result = (
            MathCrew()
            .crew()
            .kickoff(inputs={"a": 1, "b": 2})
        )

        print("Math result generated", result.raw)


def kickoff():
    wikipedia_flow = WikipediaFlow()
    wikipedia_flow.kickoff()


def plot():
    wikipedia_flow = WikipediaFlow()
    wikipedia_flow.plot()


if __name__ == "__main__":
    kickoff()
