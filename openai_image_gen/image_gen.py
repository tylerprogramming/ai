from openai import OpenAI
import base64
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"), 
    organization=os.getenv("OPENAI_ORGANIZATION")
)

prompt = """
    A studio ghibli style drawing of a cat in a business 
    suit with 4 ninja cats surrounding him ready to attack.
"""

result = client.images.generate(
    model="gpt-image-1",
    prompt=prompt
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

# Save the image to a file
with open("images_output/cat.png", "wb") as f:
    f.write(image_bytes)
    
    
    
    
