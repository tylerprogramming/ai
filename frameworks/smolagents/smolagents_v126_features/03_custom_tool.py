"""
Smolagents Custom Tool Example

Creating custom tools for agents.
"""

from smolagents import CodeAgent, Tool, LiteLLMModel


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
            allowed_names = {
                "abs": abs, "round": round, "min": min, "max": max,
                "sum": sum, "pow": pow,
            }
            result = eval(expression, {"__builtins__": {}}, allowed_names)
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
