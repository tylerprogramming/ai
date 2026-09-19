# Infographic Creation with OpenAI and Airtable

This project is designed to generate infographics based on a given topic using the OpenAI API for image generation and Airtable for storing the generated images. The process is managed through a flow-based architecture using the `crewai.flow` library.

## Overview of main.py

The `main.py` script is the core of the infographic creation process. It orchestrates the generation of infographics by interacting with OpenAI and Airtable APIs.

### Key Components

1. **Environment Setup**:
   - Utilizes the `dotenv` library to load environment variables, including API keys and configuration settings for OpenAI and Airtable.

2. **Data Models**:
   - **InfographicStep** and **InfographicStepList**: Represent the steps involved in creating an infographic.
   - **InfographicKeypoint** and **InfographicKeypointList**: Represent key points to be visualized in the infographic.
   - **InfographicState**: Holds the state of the infographic creation process, including the topic, keypoints, steps, image settings, and Airtable configuration.

3. **InfographicFlow Class**:
   - Inherits from `Flow[InfographicState]` and manages the sequence of operations for generating and storing infographics.

4. **Flow Methods**:
   - **generate_infographic_keypoints**: Initiates the process by generating key points for the infographic using the `InfographicResearchCrew`.
   - **generate_infographic_images**: Listens for keypoints generation and creates images for each keypoint using the OpenAI API.
   - **generate_infographic_flow_steps**: Reads the current script file to generate a simplified list of steps involved in the flow, then creates an infographic for these steps.
   - **save_image_locally**: Saves generated images to a local directory.
   - **save_flow_to_airtable**: Uploads the generated images to Airtable, associating them with records in a specified table.

5. **Kickoff Function**:
   - The `kickoff` function initializes the `InfographicFlow` and starts the process with a given topic.

### Detailed Functionality

- **Image Generation**: Uses the OpenAI API to generate images based on key points and flow steps, specifying styles, layouts, and color palettes.
- **File Handling**: Saves images locally in a specified output directory, ensuring the directory exists before saving files.
- **Airtable Integration**: Uses the Airtable API to upload images as attachments to records in a specified table, iterating over all files in the output directory.

### Error Handling
The script includes try-except blocks to handle potential errors during image generation and file reading, ensuring that the process continues even if some operations fail.

This script is a comprehensive solution for generating and managing infographics, leveraging both AI and cloud-based storage to automate the process.
