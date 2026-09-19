# from typing import Type

# from crewai_tools import BaseTool
# from pydantic import BaseModel, Field
# from crewai_tools import LlamaIndexTool
# from llama_index.readers.wikipedia import WikipediaReader
# from llama_index.core.tools.ondemand_loader_tool import OnDemandLoaderTool

# reader = WikipediaReader()

# tool = OnDemandLoaderTool.from_defaults(
#     reader,
#     name="Wikipedia Tool",
#     description="A tool for loading data and querying articles from Wikipedia",
# )

# class WikipediaToolInput(BaseModel):
#     """Input schema for WikipediaTool."""
#     topic: str = Field(..., description="A topic to search Wikipedia with")
#     query_str: str = Field(..., description="A query string to search Wikipedia with")

# class WikipediaTool(BaseTool):
#     name: str = "Wikipedia Tool"
#     description: str = (
#         "A tool for loading data and querying articles from Wikipedia"
#     )
#     args_schema: Type[BaseModel] = WikipediaToolInput

#     def _run(self, topic: str, query_str: str) -> str:
#         result = tool([topic], query_str=query_str)
#         return result
