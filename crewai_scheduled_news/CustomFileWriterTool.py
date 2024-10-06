from crewai_tools import BaseTool
import os
from agentops import record_tool

class CustomFileWriterTool(BaseTool):
    name: str = "Custom File Writer Tool"
    description: str = "Write content to a file."

    @record_tool(name="Custom File Writer Tool")
    def _run(self, filename: str, content: str) -> str:
        # Ensure the filename has a .md extension
        if not filename.endswith('.md'):
            filename += '.md'

        # Create the 'output' directory if it doesn't exist
        output_dir = 'ainews'
        os.makedirs(output_dir, exist_ok=True)

        # Combine the output directory with the filename
        file_path = os.path.join(output_dir, filename)

        try:
            # Write the content to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            return f"The content has been successfully written to the file: {file_path}"
        except Exception as e:
            return f"An error occurred while writing to the file: {str(e)}"