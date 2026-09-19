#!/usr/bin/env python
from pydantic import BaseModel
import base64
from openai import OpenAI
from dotenv import load_dotenv
import os
from pyairtable import Api
from pathlib import Path

from crewai.flow import Flow, listen, start, or_
from .crews.infographic_research_crew.infographic_research_crew import InfographicResearchCrew

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), organization=os.getenv("OPENAI_ORGANIZATION"))

class InfographicStep(BaseModel):
    step: str

class InfographicStepList(BaseModel):
    steps: list[InfographicStep]

class InfographicKeypoint(BaseModel):
    keypoint: str
    image_name: str

class InfographicKeypointList(BaseModel):
    keypoints: list[InfographicKeypoint]

class InfographicState(BaseModel):
    infographic_topic: str = ""
    infographic_keypoints: InfographicKeypointList = InfographicKeypointList(keypoints=[])
    infographic_steps: InfographicStepList = InfographicStepList(steps=[])
    image_resolution: str = "1536x1024"
    image_quality: str = "high"
    image_model: str = "gpt-image-1"
    airtable_api_key: str = os.getenv("AIRTABLE_API_KEY")
    airtable_base_id: str = os.getenv("AIRTABLE_BASE_ID")
    airtable_table_id: str = os.getenv("AIRTABLE_TABLE_ID")
    output_dir: str = "images_infographic_output"

class InfographicFlow(Flow[InfographicState]):
    @start()
    def generate_infographic_keypoints(self):
        result = (
            InfographicResearchCrew()
            .crew()
            .kickoff(inputs={"infographic_topic": self.state.infographic_topic})
        )

        self.state.infographic_keypoints = result.pydantic

    @listen(generate_infographic_keypoints)
    def generate_infographic_images(self):
        for keypoint in self.state.infographic_keypoints.infographic_keypoints:
            try:
                result = client.images.generate(
                    model=self.state.image_model,
                    prompt=f"""Generate an infographic explaining the concept: {keypoint.keypoint}
                        Style: Isometric illustration OR Vibrant cartoon style OR Minimalist line art.
                        Key Visuals: Include icons/graphics representing [mention 2-3 core concepts implied by the keypoint, if possible. E.g., if keypoint is 'Exercise boosts mood', visuals could be a person running, a smiling brain icon, upward trending arrow].
                        Layout: Vertical flow with the keypoint as the main title.
                        Color Palette: Use bright and engaging colors OR a professional blue and green palette.""",
                    size=self.state.image_resolution,
                    quality=self.state.image_quality,
                )

                self.save_image_locally(self, keypoint.image_name, result)
            except Exception as e:
                print(f"Error generating image: {e}")
                continue

    @listen(generate_infographic_keypoints)
    def generate_infographic_flow_steps(self):
        try:
            with open(__file__, 'r') as file:
                contents = file.read()
                
            completion = client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",
                messages=[
                    {"role": "system", "content": "I need all the steps simplified in under 5 words of the flow involved in the crewai flow file provided.  Only return the steps, no other text."},
                    {"role": "user", "content": contents},
                ],
                response_format=InfographicStepList,
            )

            self.state.infographic_steps = completion.choices[0].message.parsed.steps

            result = client.images.generate(
                model=self.state.image_model,
                prompt=f"""Generate an infographic explaining the concept: {self.state.infographic_steps}.
                    Style: Isometric illustration OR Vibrant cartoon style OR Minimalist line art.""",
                size=self.state.image_resolution,
                quality=self.state.image_quality,
            )

            self.save_image_locally(self, "infographic_flow", result)
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
        
        print(self.state)

    @listen(or_(generate_infographic_images, generate_infographic_flow_steps))
    def save_image_locally(self, image_name, result):
        print(f"Saving image: {image_name}")
        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        os.makedirs(self.state.output_dir, exist_ok=True)

        # Save the image to a file
        with open(f"{self.state.output_dir}/{image_name}.png", "wb") as f:
            f.write(image_bytes)

    @start()
    def save_flow_to_airtable(self):
        api = Api(self.state.airtable_api_key)
        base = api.base(self.state.airtable_base_id)
        table = base.table(self.state.airtable_table_id)

        # Iterate over all files in the directory
        directory_path = Path(self.state.output_dir)
        for file_path in directory_path.iterdir():
            if file_path.is_file():
                with file_path.open('rb') as file:
                    response = table.create(
                        fields={
                            "image_name": file_path.name
                        }
                    )

                    table.upload_attachment(
                        record_id=response['id'],
                        field="Attachments",
                        filename=f"{directory_path}/{file_path.name}",
                    )

def kickoff(topic: str):
    infographic_flow = InfographicFlow()
    infographic_flow.kickoff(inputs={"infographic_topic": topic})

