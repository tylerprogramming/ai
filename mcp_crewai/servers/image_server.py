from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from openai import OpenAI
import os
import base64

# Initialize FastMCP server
mcp = FastMCP("image_server")

output_dir = "images"

@mcp.tool(name="image_creation_openai", description="Create an image using OpenAI's Images API")
def image_creation_openai(query: str, image_name: str) -> str:
    """Create an image using OpenAI's Images API"""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), organization=os.getenv("OPENAI_ORGANIZATION"))
    
    try:
        result = client.images.generate(
            model="gpt-image-1",
            prompt=f"""Generate an image based on the following prompt: {query}""",
            size="1024x1024",
            quality="high",
        )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        os.makedirs(output_dir, exist_ok=True)

        # Save the image to a file
        with open(f"{output_dir}/{image_name}.png", "wb") as f:
            f.write(image_bytes)
            
        return {"success": True, "url": result.data[0].url}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    mcp.run(transport="stdio")
    print("Image Creation MCP Server running stdio")