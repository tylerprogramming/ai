#!/usr/bin/env python
from typing import List
from pydantic import BaseModel
from openai import OpenAI
from crewai.flow import Flow, listen, start, router
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.utils import make_chunks
from pathlib import Path
from dotenv import load_dotenv
from pyairtable import Api
from llama_cloud_services import LlamaParse
import nest_asyncio
import os

from googledrive.src.googledrive.crews.meeting_minutes_crew.meeting_minutes_crew import MeetingMinutesCrew
from googledrive.src.googledrive.crews.contractmanagement.contractmanagement import Contractmanagement

nest_asyncio.apply()

load_dotenv()

client = OpenAI()

class GoogleDriveOutput(BaseModel):
    final_summary: str = ""
    file_name: str = ""
    telegram_message: str = ""

class GoogleDriveState(BaseModel):
    summary: str = ""
    file_name: str = ""
    file_type: str = ""
    types: List[str] = ['meeting', 'project', 'contract', 'other']

class GoogleDriveFlow(Flow[GoogleDriveState]):

    @start()
    def retrieve_types(self):
        print("Retrieving types")
        print("File name", self.state.file_name)
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"Based on the file name: {self.state.file_name}, determine the type of the file.  The types are {self.state.types}. ONLY return the type."
                }
            ]
        )
        
        self.state.file_type = completion.choices[0].message.content
        
    @router(retrieve_types)
    def routing_type(self):
        print("Routing type: ", self.state.file_type)
        if self.state.file_type == "meeting":
            return "meeting_minutes"
        else:
            return "contract_management"

    @listen("meeting_minutes")
    def meeting_minutes_extraction(self):
        print("Begin Meeting minutes extraction...")

        SCRIPT_DIR = Path(__file__).parent.parent.parent.parent / "downloads"
        audio_path = str(SCRIPT_DIR / self.state.file_name)
        
        # Load the audio file
        audio = AudioSegment.from_file(audio_path, format="wav")
        
        # Define chunk length in milliseconds (e.g., 1 minute = 60,000 ms)
        chunk_length_ms = 60000
        chunks = make_chunks(audio, chunk_length_ms)

        # Transcribe each chunk
        full_transcription = ""
        for i, chunk in enumerate(chunks):
            print(f"Transcribing chunk {i+1}/{len(chunks)}")
            chunk_path = f"chunk_{i}.wav"
            chunk.export(chunk_path, format="wav")
            
            with open(chunk_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
                full_transcription += transcription.text + " "
        
        result = (
            MeetingMinutesCrew()
            .crew()
            .kickoff(inputs={"transcript": full_transcription})
        )
        
        return GoogleDriveOutput(
            final_summary=result.raw,
            file_name=self.state.file_name,
            telegram_message=f"📄 New Meeting Minutes uploaded: {self.state.file_name}"
        )

    @listen("contract_management")
    def contract_management_extraction(self):
        print("Begin Contract management extraction...")

        SCRIPT_DIR = Path(__file__).parent.parent.parent.parent / "downloads"
        pdf_path = str(SCRIPT_DIR / self.state.file_name)

        parser = LlamaParse(
            api_key=os.getenv("LLAMA_API_KEY"),
            result_type="markdown"
        )
        
        documents = parser.load_data(pdf_path)
        
        result = (
            Contractmanagement()
            .crew()
            .kickoff(inputs={"contract_content": documents[0].text_resource.text})
        )
        
        return GoogleDriveOutput(
            final_summary=result.raw,
            file_name=self.state.file_name,
            telegram_message=f"📄 New Contract uploaded: {self.state.file_name}"
        )
    

def kickoff(file_name: str):
    print("Kicking off with file name", file_name)
    print(os.getenv("AIRTABLE_API_KEY"))
    drive_flow = GoogleDriveFlow()
    inputs = {
        "file_name": file_name
    }
    
    response = drive_flow.kickoff(inputs)
    
    airtable_api_key = os.getenv("AIRTABLE_API_KEY")
    airtable_base_id = os.getenv("AIRTABLE_BASE_ID")
    airtable_table_name = os.getenv("AIRTABLE_TABLE_NAME")
    
    COLUMN_NAMES = ['file_name', 'final_summary', 'telegram_message']
    COLUMN_DATA = [response.file_name, response.final_summary, response.telegram_message]
    
    # Create record dictionary using dict comprehension with zip
    record_data = dict(zip(COLUMN_NAMES, COLUMN_DATA))
    
    api = Api(airtable_api_key)
    base = api.base(airtable_base_id)
    table = base.table(airtable_table_name)
    
    table.create(record_data)

    return response.telegram_message


if __name__ == "__main__":
    kickoff()
