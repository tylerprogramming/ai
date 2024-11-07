#!/usr/bin/env python
from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start
from crews.wikipedia_crew.wikipedia_crew import WikipediaCrew
from crews.yahoo_crew.yahoo_crew import YahooCrew
from crews.math_crew.crew import MathCrew

class CustomState(BaseModel):
    topic: str = ""
    query_str: str = ""
    wikipedia_result: str = ""
    yahoo_result: str = ""
    math_result: str = ""

class CustomFlow(Flow[CustomState]):
    @start()
    def generate_topic(self):
        print("Generating topic")
        self.state.topic = "San Francisco"

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
    def yahoo_finance_query(self):
        print("Generating yahoo finance query")
        result = (
            YahooCrew()
            .crew()
            .kickoff(inputs={"query": "AAPL"})
        )

        self.state.yahoo_result = result.raw

    @listen(yahoo_finance_query)
    def generate_math_result(self):
        print("Generating math result")
        result = (
            MathCrew()
            .crew()
            .kickoff(inputs={"a": 5, "b": 2})
        )

        self.state.math_result = result.raw

def kickoff():
    custom_flow = CustomFlow()
    custom_flow.kickoff()
    print(custom_flow.state)

def plot():
    custom_flow = CustomFlow()
    custom_flow.plot()

if __name__ == "__main__":
    kickoff()
    plot()
