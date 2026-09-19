import dotenv
import whisper
from moviepy.editor import *
from openai import OpenAI

dotenv.load_dotenv()


def recognize_transcript_from_video(audio_filepath):
    try:
        # Load model
        model = whisper.load_model("small")

        # Transcribe audio with detailed timestamps
        result = model.transcribe(audio_filepath, verbose=True)

        # Initialize variables for transcript
        transcript = []
        sentence = ""
        start_time = 0

        # Iterate through the segments in the result
        for segment in result['segments']:
            # If new sentence starts, save the previous one and reset variables
            if segment['start'] != start_time and sentence:
                transcript.append({
                    "sentence": sentence.strip() + ".",
                    "timestamp_start": start_time,
                    "timestamp_end": segment['start']
                })
                sentence = ""
                start_time = segment['start']

            # Add the word to the current sentence
            sentence += segment['text'] + " "

        # Add the final sentence
        if sentence:
            transcript.append({
                "sentence": sentence.strip() + ".",
                "timestamp_start": start_time,
                "timestamp_end": result['segments'][-1]['end']
            })

        # Save the transcript to a file
        with open("transcription.txt", "w") as file:
            for item in transcript:
                sentence = item["sentence"]
                start_time, end_time = item["timestamp_start"], item["timestamp_end"]

                file.write(f"{start_time}s to {end_time}s: {sentence}\n")

        return transcript

    except FileNotFoundError as f:
        return f"The specified audio file could not be found: {str(f)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


def translate_text(input_text, source_language, target_language):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model=os.getenv("model"),
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",
             "content": f"Directly translate the following {source_language} text to a pure {target_language} "
                        f"video subtitle text without additional explanation.: '{input_text}'"},
        ],
        max_tokens=1500
    )

    # Correctly accessing the response content
    translated_text = response.choices[0].message.content if response.choices else None

    return translated_text


def translate_transcript(source_language, target_language):
    with open("transcription.txt", "r") as f:
        lines = f.readlines()

    translated_transcript = []

    for line in lines:
        # Split each line into timestamp and text parts
        parts = line.strip().split(': ')
        if len(parts) == 2:
            timestamp, text = parts[0], parts[1]

            translated_text = translate_text(text, source_language, target_language)
            translated_line = f"{timestamp}: {translated_text}"
            translated_transcript.append(translated_line)
        else:
            translated_transcript.append(line.strip())

    with open(f"{target_language}_transcription.txt", "w") as file:
        for line in translated_transcript:
            file.write(f"{line}\n")

    return '\n'.join(translated_transcript)
