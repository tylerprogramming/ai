# Example 1: Initialize from FunctionTool
from llama_index.core.tools import FunctionTool
from crewai_tools import LlamaIndexTool
from pydantic import BaseModel, Field
from typing import Type
from crewai_tools import BaseTool

def math_tool(a: int, b: int) -> int:
    return a * b

class MathToolInput(BaseModel):
    """Input schema for MathTool."""
    a: int = Field(..., description="A number to multiply")
    b: int = Field(..., description="Another number to multiply")

og_tool = FunctionTool.from_defaults(
    math_tool, 
    name="math_tool", 
    description='A tool for multiplying two numbers',
    fn_schema=MathToolInput
)

tool = LlamaIndexTool.from_tool(og_tool)

