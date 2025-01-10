from smolagents import CodeAgent, HfApiModel
from smolagents import tool, Tool
from huggingface_hub import InferenceClient
from huggingface_hub import list_models
import gradio as gr
from dotenv import load_dotenv
import PIL.Image

load_dotenv()

@tool
def model_download_tool(task: str) -> str:
    """
    This is a tool that returns the most downloaded model of a given task on the Hugging Face Hub.
    It returns the name of the checkpoint.

    Args:
        task: The task for which to get the download count.
    """
    most_downloaded_model = next(iter(list_models(filter=task, sort="downloads", direction=-1)))
    
    return most_downloaded_model.id

class TextToImageTool(Tool):
    description = "This tool creates an image according to a prompt, which is a text description."
    name = "image_generator"
    inputs = {
        "prompt": {
            "type": "string", 
            "description": "The image generator prompt. Don't hesitate to add details in the prompt to make the image look better, like 'high-res, photorealistic', etc."
        },
        "model": {
            "type": "string",
            "description": "The Hugging Face model ID to use for image generation. If not provided, will use the default model."
        }
    }
    output_type = "image"
    current_model = "black-forest-labs/FLUX.1-schnell"

    def forward(self, prompt, model):
        if model:
            if model != self.current_model:
                self.current_model = model
                self.client = InferenceClient(model)
        if not self.client:
            self.client = InferenceClient(self.current_model)
            
        image = self.client.text_to_image(prompt)
        image.save("image.png")
            
        return f"Successfully saved image with this prompt: {prompt} using model: {self.current_model}"

def generate_image(prompt):
    """
    Function to handle the Gradio interface interaction
    """
    image_generator = TextToImageTool()
    agent = CodeAgent(tools=[image_generator, model_download_tool], model=HfApiModel())
    
    # Run the agent with the provided prompt
    result = agent.run(
        f"Improve this prompt, then generate an image of it. Prompt: {prompt}. Get the latest model for text-to-image from the Hugging Face Hub."
    )
    
    # Load and return the generated image along with the result text
    generated_image = PIL.Image.open("image.png")
    return generated_image, result

# Create Gradio interface
demo = gr.Interface(
    fn=generate_image,
    inputs=[
        gr.Textbox(
            label="Enter your image prompt",
            placeholder="Example: A cat wearing a hazmat suit in contaminated area"
        )
    ],
    outputs=[
        gr.Image(label="Generated Image"),
        gr.Textbox(label="Agent Response")
    ],
    title="AI Image Generator",
    description="Enter a prompt and the AI will improve it and generate an image using the latest text-to-image model.",
    examples=[
        ["A cat wearing a hazmat suit in contaminated area"],
        ["A peaceful garden with butterflies"],
        ["A futuristic city at night"]
    ]
)

# Launch the interface
if __name__ == "__main__":
    demo.launch()