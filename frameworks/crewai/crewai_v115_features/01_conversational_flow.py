"""
CrewAI v1.15+ Conversational Flow Example

Interactive chat-style agent workflows that maintain conversation state.

Decorating a Flow with @ConversationConfig turns it into a conversational flow:
each user message is one "turn", the message history lives in self.state.messages,
and an LLM router picks which @listen("<route>") handler answers the turn.
Built-in routes: "converse" (plain chat over the history) and "end" (goodbye).
"""

from crewai import Agent, Task, Crew, Process, LLM
from crewai.flow import Flow, ConversationConfig, listen

llm = LLM(model="gpt-5.4-mini")


@ConversationConfig(
    llm=llm,  # used for routing and for the built-in "converse" route
    system_prompt="You are a friendly AI assistant. Keep answers short and helpful.",
)
class ConversationalAssistant(Flow):
    """A conversational flow that handles multi-turn interactions."""

    @listen("research")
    def handle_research(self):
        """Questions that need a careful, researched answer from the research agent."""
        researcher = Agent(
            role="Research Assistant",
            goal="Help users find accurate information",
            backstory="Expert researcher with access to vast knowledge",
            llm=llm,
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

        # The returned text becomes the assistant's reply for this turn
        result = crew.kickoff(inputs={"query": self.state.current_user_message})
        return result.raw


def main():
    flow = ConversationalAssistant()
    print("Hello! I'm your AI assistant. How can I help you today? (type 'exit' to quit)")

    # chat() runs an interactive terminal loop; each message calls flow.handle_turn()
    flow.chat()

    # For web apps / scripts, call handle_turn() directly instead:
    #   reply = flow.handle_turn("What are the key features of CrewAI v1.15?")


if __name__ == "__main__":
    main()
