from llama_index.core.tools import FunctionTool
from crewai_tools import LlamaIndexTool
from pydantic import BaseModel, Field

def add(a: int, b: int) -> int:
    return a + b

def subtract(a: int, b: int) -> int:
    return a - b

def multiply(a: int, b: int) -> int:
    return a * b

def divide(a: int, b: int) -> int:
    return a / b

class MathToolInput(BaseModel):
    """Input schema for MathTool."""
    a: int = Field(..., description="The first number")
    b: int = Field(..., description="The second number")

add_tool = FunctionTool.from_defaults(
    add, 
    name="add_tool", 
    description='A tool for adding two numbers',
    fn_schema=MathToolInput
)

subtract_tool = FunctionTool.from_defaults(
    subtract, 
    name="subtract_tool", 
    description='A tool for subtracting two numbers',
    fn_schema=MathToolInput
)

multiply_tool = FunctionTool.from_defaults(
    multiply, 
    name="multiply_tool", 
    description='A tool for multiplying two numbers',
    fn_schema=MathToolInput
)

divide_tool = FunctionTool.from_defaults(
    divide, 
    name="divide_tool", 
    description='A tool for dividing two numbers',
    fn_schema=MathToolInput
)

my_add_tool = LlamaIndexTool.from_tool(add_tool)
my_subtract_tool = LlamaIndexTool.from_tool(subtract_tool)
my_multiply_tool = LlamaIndexTool.from_tool(multiply_tool)
my_divide_tool = LlamaIndexTool.from_tool(divide_tool)

my_tools = [my_add_tool, my_subtract_tool, my_multiply_tool, my_divide_tool]

