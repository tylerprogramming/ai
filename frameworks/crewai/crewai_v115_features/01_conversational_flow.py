"""
CrewAI v1.15+ Conversational Flow Example

Interactive chat-style agent workflows that maintain conversation state.
"""

from crewai import Agent, Task, Crew, Process, LLM
from crewai.flow import Flow, listen, start


class ConversationalAssistant(Flow):
    """A conversational flow that handles multi-turn interactions."""

    def __init__(self):
        super().__init__()
        self.conversation_history = []
        self.llm = LLM(model="gpt-5.4-mini")

    @start()
    def greet(self):
        """Start the conversation with a greeting."""
        self.conversation_history.append({"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"})
        return "greeting_complete"

    @listen(greet)
    def process_request(self, _):
        """Process user requests using a research agent."""
        researcher = Agent(
            role="Research Assistant",
            goal="Help users find accurate information",
            backstory="Expert researcher with access to vast knowledge",
            llm=self.llm,
            verbose=True,
        )

        research_task = Task(
            description="Research and provide helpful information based on the user's query: {query}",
            expected_output="Clear, accurate response to the user's question",
            agent=researcher,
        )

        crew = Crew(
            agents=[researcher],
            tasks=[research_task],
            process=Process.sequential,
            verbose=True,
        )

        return crew


def main():
    flow = ConversationalAssistant()
    result = flow.kickoff(inputs={"query": "What are the key features of CrewAI v1.15?"})
    print(f"\nResult: {result}")


if __name__ == "__main__":
    main()
