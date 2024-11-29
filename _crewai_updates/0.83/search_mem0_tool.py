from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from mem0 import MemoryClient

client = MemoryClient(api_key="m0-sblhjtHFcj96vR7GAvPwQ5sVgY5J5pifrYrybXLA")

class SearchMem0ToolInput(BaseModel):
    """Input schema for AirtableTool."""
    query: str = Field(..., description="This is a query you want to search the memory store with.")

class SearchMem0Tool(BaseTool):
    name: str = "SearchMem0Tool"
    description: str = (
        "Clear description for what this tool is useful for, you agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = SearchMem0ToolInput

    def _run(self, query: str) -> str:
        result = client.search(query, user_id="tyler")
        return result
