"""
Smolagents Custom Tool Example

Creating custom tools for agents.
"""

import ast
import operator

from smolagents import CodeAgent, Tool, LiteLLMModel

# Safe arithmetic: walk the expression's syntax tree and allow only numbers,
# arithmetic operators and a few math functions. No eval() on model input.
_OPERATORS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod,
    ast.Pow: operator.pow, ast.USub: operator.neg, ast.UAdd: operator.pos,
}
_FUNCTIONS = {"abs": abs, "round": round, "min": min, "max": max, "sum": sum, "pow": pow}


def safe_eval(expression: str):
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
            left, right = _eval(node.left), _eval(node.right)
            if isinstance(left, list) or isinstance(right, list):
                raise ValueError("lists are only allowed as function arguments, e.g. sum([1, 2])")
            if isinstance(node.op, ast.Pow) and abs(right) > 100:
                raise ValueError("exponent too large")
            return _OPERATORS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
            return _OPERATORS[type(node.op)](_eval(node.operand))
        if isinstance(node, (ast.List, ast.Tuple)):
            return [_eval(e) for e in node.elts]
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id in _FUNCTIONS and not node.keywords):
            return _FUNCTIONS[node.func.id](*[_eval(a) for a in node.args])
        raise ValueError(f"unsupported expression: {ast.dump(node)[:60]}")

    return _eval(ast.parse(expression, mode="eval"))


class CalculatorTool(Tool):
    """A calculator tool for mathematical operations."""
    
    name = "calculator"
    description = "Performs mathematical calculations. Input should be a mathematical expression."
    inputs = {
        "expression": {
            "type": "string",
            "description": "The mathematical expression to evaluate (e.g., '2 + 2 * 3')"
        }
    }
    output_type = "string"

    def forward(self, expression: str) -> str:
        try:
            result = safe_eval(expression)
            return f"Result: {result}"
        except Exception as e:
            return f"Error: {str(e)}"


class UnitConverterTool(Tool):
    """Convert between common units."""
    
    name = "unit_converter"
    description = "Converts values between different units (length, weight, temperature)."
    inputs = {
        "value": {"type": "number", "description": "The value to convert"},
        "from_unit": {"type": "string", "description": "Source unit (e.g., 'km', 'miles', 'celsius')"},
        "to_unit": {"type": "string", "description": "Target unit (e.g., 'miles', 'km', 'fahrenheit')"},
    }
    output_type = "string"

    def forward(self, value: float, from_unit: str, to_unit: str) -> str:
        conversions = {
            ("km", "miles"): lambda x: x * 0.621371,
            ("miles", "km"): lambda x: x * 1.60934,
            ("celsius", "fahrenheit"): lambda x: x * 9/5 + 32,
            ("fahrenheit", "celsius"): lambda x: (x - 32) * 5/9,
            ("kg", "lbs"): lambda x: x * 2.20462,
            ("lbs", "kg"): lambda x: x / 2.20462,
        }
        
        key = (from_unit.lower(), to_unit.lower())
        if key in conversions:
            result = conversions[key](value)
            return f"{value} {from_unit} = {result:.2f} {to_unit}"
        return f"Conversion from {from_unit} to {to_unit} not supported"


def main():
    model = LiteLLMModel(model_id="gpt-5.4-mini")

    agent = CodeAgent(
        tools=[CalculatorTool(), UnitConverterTool()],
        model=model,
        max_steps=5,
    )

    result = agent.run(
        "If I run a marathon (42.195 km), how many miles is that? "
        "Also, calculate 42.195 * 0.621371 to verify."
    )

    print(f"\nResult: {result}")


if __name__ == "__main__":
    main()
