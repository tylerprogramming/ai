# OpenAI Image Generation and Editing

This project utilizes the OpenAI API to perform various image-related tasks, including image generation, editing, inpainting, and creating images with transparent backgrounds. The project is structured into several Python scripts, each handling a specific task.

## Prerequisites

- **Python 3.x**
- **OpenAI API key and organization ID**
- **Environment variables** set for `OPENAI_API_KEY` and `OPENAI_ORGANIZATION`
- **Required Python packages**: `openai`, `python-dotenv`, `pydantic`
- If you get this error:
  ```
  openai.PermissionDeniedError: Error code: 403 - {'error': {'message': 'To access gpt-image-1, please complete organization verification: https://help.openai.com/en/articles/10910291-api-organization-verification', 'type': 'invalid_request_error', 'param': None, 'code': None}}
  ```
  then you need to do this:
  To access the `gpt-image-1` model, organization verification is required. Please complete the verification process as described [here](https://help.openai.com/en/articles/10910291-api-organization-verification).

## Setup

1. **Clone the repository**.
2. **Install the required packages**:
   ```bash
   pip install openai python-dotenv pydantic
   ```
3. **Set up your environment variables** in a `.env` file:
   ```
   OPENAI_API_KEY=your_api_key
   OPENAI_ORGANIZATION=your_organization_id
   ```

## Scripts

### 1. Image Generation (`image_gen.py`)

Generates a Studio Ghibli style image of a cat in a business suit with ninja cats. :D

- **Output**: `images_output/cat.png`

### 2. Image Editing (`image_editing.py`)

Edits images to create a photorealistic image of a gift basket with specific items.

- **Input**: Images from `images_edit/`
- **Output**: `images_output/gift-basket.png`

### 3. Image Inpainting (`image_inpainting.py`)

Performs inpainting on an image to add a flamingo to a sunlit indoor lounge area.

- **Input**: `images_inpainting/sunlit_lounge.png` and `images_inpainting/mask.png`
- **Output**: `images_output/composition.png`

### 4. Image Transparent Background (`image_transparent_background.py`)

Generates pixel art style images with transparent backgrounds based on prompts.

- **Output**: Images saved in `images_pixel_art_output/`

## Important Note

To access the `gpt-image-1` model, organization verification is required. Please complete the verification process as described [here](https://help.openai.com/en/articles/10910291-api-organization-verification).