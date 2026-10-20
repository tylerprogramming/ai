from mcp.server.fastmcp import FastMCP
from openai import OpenAI
import os
import sys
import base64

# Initialize FastMCP server
mcp = FastMCP("image_server")

# Save images in the project's images/ folder, wherever the server is started from
output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")

@mcp.tool(name="image_creation_openai", description="Create an image using OpenAI's Images API")
def image_creation_openai(query: str, image_name: str) -> dict:
    """Create an image using OpenAI's Images API"""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), organization=os.getenv("OPENAI_ORGANIZATION"))
    
    try:
        result = client.images.generate(
            model="gpt-image-2.5-flare",  # gpt-image-1 shuts down 2026-10-23
            prompt=f"""Generate an image based on the following prompt: {query}""",
            size="1024x1024",
            quality="high",
        )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        os.makedirs(output_dir, exist_ok=True)

        # Save the image to a file
        image_path = os.path.join(output_dir, f"{image_name}.png")
        with open(image_path, "wb") as f:
            f.write(image_bytes)

        # GPT image models return base64 only (no URL), so return where the file was saved
        return {"success": True, "path": image_path}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # stdout carries the MCP protocol, so log to stderr
    print("Image Creation MCP Server running stdio", file=sys.stderr)
    mcp.run(transport="stdio")