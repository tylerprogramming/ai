#!/usr/bin/env python
import json
import os
from typing import Dict, Optional, List
from pydantic import BaseModel, Field
from crewai import LLM
from crewai.flow.flow import Flow, listen, start
from firecrawl import FirecrawlApp, ScrapeOptions
from dotenv import load_dotenv
from guide_creator_flow.crews.content_crew.content_crew import ContentCrew
from guide_creator_flow.models.guides import GuideOutline, WebResearch

load_dotenv()

class GuideCreatorState(BaseModel):
    topic: str = ""
    audience_level: str = ""
    web_research: List[WebResearch] = Field(default_factory=list)
    guide_outline: Optional[GuideOutline] = None
    sections_content: Dict[str, str] = Field(default_factory=dict)

class GuideCreatorFlow(Flow[GuideCreatorState]):

    @start()
    def set_user_inputs(self):
        """Get input from the user about the guide topic and audience"""
        print(f"\nCreating a guide on {self.state.topic} for {self.state.audience_level} audience...\n")
        
        print(f"Topic: {self.state.topic}")
        print(f"Audience level: {self.state.audience_level}")
        
        return self.state
    
    @listen(set_user_inputs)
    def web_research(self):
        """Perform web research for the guide topic"""
        print("Performing web research...")

        app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

        search_result = app.search(
            query=self.state.topic,
            limit=5,
            tbs="qdr:w",
            scrape_options=ScrapeOptions(formats=["markdown", "links"])
        )

        web_research = []

        # Print the search results
        for result in search_result.data:
            web_research.append(WebResearch(
                search_results_title=result['title'],
                search_results_url=result['url'],
                search_results_description=result['description'],
                search_results_content=result['markdown'],
                search_results_links=result['links']
            ))
            print(result['title'])
            print(result['url'])
            print(result['description'])
            print(result['markdown'][:150] + "...")
            print(result['links'])
            print("-"*100)
        
        self.state.web_research = web_research
        return self.state

    @listen(web_research)
    def create_guide_outline(self, state):
        """Create a structured outline for the guide using a direct LLM call"""
        print("Creating guide outline...")

        # Initialize the LLM
        llm = LLM(model="openai/gpt-5", response_format=GuideOutline)

        # Create the messages for the outline
        messages = [
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": f"""
            Create a detailed outline for a comprehensive guide on "{state.topic}" for {state.audience_level} level learners.

            The outline should include:
            1. A compelling title for the guide
            2. An introduction to the topic
            3. 4-6 main sections that cover the most important aspects of the topic
            4. A conclusion or summary

            For each section, provide a clear title and a brief description of what it should cover.
            Use the web research to help you create the guide outline as context: {state.web_research}
            """}
        ]

        # Make the LLM call with JSON response format
        response = llm.call(messages=messages)

        # Parse the JSON response handling both str and dict responses
        if isinstance(response, str):
            outline_dict = json.loads(response)
        elif isinstance(response, dict):
            outline_dict = response
        else:
            outline_dict = json.loads(str(response))
        self.state.guide_outline = GuideOutline(**outline_dict)

        # Ensure output directory exists before saving
        os.makedirs("output", exist_ok=True)

        # Save the outline to a file
        with open("output/guide_outline.json", "w") as f:
            json.dump(outline_dict, f, indent=2)

        print(f"Guide outline created with {len(self.state.guide_outline.sections)} sections")
        return self.state.guide_outline

    @listen(create_guide_outline)
    def write_and_compile_guide(self, outline):
        """Write all sections and compile the guide"""
        print("Writing guide sections and compiling...")
        completed_sections = []

        # Process sections one by one to maintain context flow
        for section in outline.sections:
            print(f"Processing section: {section.title}")

            # Build context from previous sections
            previous_sections_text = ""
            if completed_sections:
                previous_sections_text = "# Previously Written Sections\n\n"
                for title in completed_sections:
                    previous_sections_text += f"## {title}\n\n"
                    previous_sections_text += self.state.sections_content.get(title, "") + "\n\n"
            else:
                previous_sections_text = "No previous sections written yet."

            # Run the content crew for this section
            result = ContentCrew().crew().kickoff(inputs={
                "section_title": section.title,
                "section_description": section.description,
                "audience_level": self.state.audience_level,
                "previous_sections": previous_sections_text,
                "draft_content": ""
            })

            # Store the content (handle different return shapes)
            section_text = getattr(result, "raw", None)
            if section_text is None and isinstance(result, dict):
                section_text = result.get("raw")
            if section_text is None:
                section_text = str(result)

            self.state.sections_content[section.title] = section_text
            completed_sections.append(section.title)
            print(f"Section completed: {section.title}")

        # Compile the final guide
        guide_content = f"# {outline.title}\n\n"
        guide_content += f"## Introduction\n\n{outline.introduction}\n\n"

        # Add each section in order
        for section in outline.sections:
            section_content = self.state.sections_content.get(section.title, "")
            guide_content += f"\n\n{section_content}\n\n"

        # Add conclusion
        guide_content += f"## Conclusion\n\n{outline.conclusion}\n\n"

        # Save the guide
        with open("output/complete_guide.md", "w") as f:
            f.write(guide_content)

        print("\nComplete guide compiled and saved to output/complete_guide.md")
        return "Guide creation completed successfully"


def kickoff():
    """Run the guide creator flow"""
    print("\n=== Create Your Comprehensive Guide ===\n")

    # Get user input
    topic = input("What topic would you like to create a guide for? ")

    # Get audience level with validation
    while True:
        audience = input("Who is your target audience? (beginner/intermediate/advanced) ").lower()
        if audience in ["beginner", "intermediate", "advanced"]:
            audience_level = audience
            break
        else:
            print("Please enter 'beginner', 'intermediate', or 'advanced'")
        
    inputs = {
        "topic": topic,
        "audience_level": audience_level
    }
    
    GuideCreatorFlow().kickoff(inputs=inputs)
    print("\n=== Flow Complete ===")
    print("Your comprehensive guide is ready in the output directory.")
    print("Open output/complete_guide.md to view it.")

def plot():
    """Generate a visualization of the flow"""
    flow = GuideCreatorFlow()
    flow.plot("guide_creator_flow")
    print("Flow visualization saved to guide_creator_flow.html")

if __name__ == "__main__":
    kickoff()
