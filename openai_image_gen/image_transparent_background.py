from openai import OpenAI
import base64
from dotenv import load_dotenv
import os
from pydantic import BaseModel

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), organization=os.getenv("OPENAI_ORGANIZATION"))

class PixelArtImagePrompt(BaseModel):
    image_prompt: str
    image_name: str

class PixelArtImagePromptList(BaseModel):
    image_prompts: list[PixelArtImagePrompt]

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "I need 2 different pixel art style hats for my indie game."},
        {"role": "user", "content": "The game will be a 2D indie game similar style to Stardew Valley.  The name shouldn't include the file extension."},
    ],
    response_format=PixelArtImagePromptList,
)

image_prompts = completion.choices[0].message.parsed.image_prompts

for image_prompt in image_prompts:
    try:
        result = client.images.generate(
            model="gpt-image-1",
            prompt=f"generate a pixel-art style picture of: {image_prompt.image_prompt}",
            size="1024x1024",
            background="transparent",
            quality="high",
        )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        # Save the image to a file
        with open(f"images_pixel_art_output/{image_prompt.image_name}.png", "wb") as f:
            f.write(image_bytes)
    except Exception as e:
        print(f"Error generating image: {e}")
        continue
