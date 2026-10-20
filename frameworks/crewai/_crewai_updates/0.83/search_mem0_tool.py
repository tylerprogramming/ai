from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from mem0 import MemoryClient
import os
from dotenv import load_dotenv

load_dotenv()  # loads MEM0_API_KEY from .env

client = MemoryClient(api_key=os.environ["MEM0_API_KEY"])

class SearchMem0ToolInput(BaseModel):
    """Input schema for SearchMem0Tool."""
    query: str = Field(..., description="This is a query you want to search the memory store with.")

class SearchMem0Tool(BaseTool):
    name: str = "SearchMem0Tool"
    description: str = (
        "Searches the user's Mem0 memory store for facts and preferences about the user."
    )
    args_schema: Type[BaseModel] = SearchMem0ToolInput

    def _run(self, query: str) -> str:
        # mem0ai 2.x: entity ids go inside `filters` for search()
        result = client.search(query, filters={"user_id": "tyler"})
        return str(result)
