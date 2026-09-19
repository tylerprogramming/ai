from pydantic import BaseModel, Field
from typing import List, Optional

class Section(BaseModel):
    title: str = Field(description="Title of the section")
    description: str = Field(description="Brief description of what the section should cover")

class GuideOutline(BaseModel):
    title: str = Field(description="Title of the guide")
    introduction: str = Field(description="Introduction to the topic")
    target_audience: str = Field(description="Description of the target audience")
    sections: List[Section] = Field(description="List of sections in the guide")
    conclusion: str = Field(description="Conclusion or summary of the guide")
    
class WebResearch(BaseModel):
    search_results_title: Optional[str] = None
    search_results_url: Optional[str] = None
    search_results_description: Optional[str] = None
    search_results_content: Optional[str] = None
    search_results_links: Optional[List[str]] = None