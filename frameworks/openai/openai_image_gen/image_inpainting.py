from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), organization=os.getenv("OPENAI_ORGANIZATION"))

result = client.images.edit(
    model="gpt-image-1",
    image=open("images_inpainting/sunlit_lounge.png", "rb"),
    mask=open("images_inpainting/mask.png", "rb"),
    prompt="A sunlit indoor lounge area with a pool containing a flamingo"
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

# Save the image to a file
with open("images_output/composition.png", "wb") as f:
    f.write(image_bytes)