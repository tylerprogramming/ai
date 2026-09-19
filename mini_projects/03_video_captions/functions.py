import dotenv
import whisper
from moviepy.editor import *

dotenv.load_dotenv()


def recognize_transcript_from_video(audio_filepath, new_file_name):
    try:
        model = whisper.load_model("medium")

        # Transcribe audio with detailed timestamps
        result = model.transcribe(audio_filepath, verbose=True)

        # Initialize variables for transcript
        transcript = []
        sentence = ""
        start_time = 0

        full_clip = VideoFileClip(audio_filepath)
        clips = []

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

        for item in transcript[1::2]:
            start_time, end_time = item["timestamp_start"], item["timestamp_end"]
            video_clip = full_clip.subclip(int(start_time), int(end_time))

            text_clip = TextClip(
                txt=item["sentence"],
                fontsize=40,
                size=(.5 * video_clip.size[0], 0),
                font="lane",
                color="black"
            )

            image_width, image_height = text_clip.size
            color_clip = ColorClip(
                size=(int(image_width * 1.1), int(image_height * 1.4)),
                color=(255, 255, 255)
            )
            color_clip = color_clip.set_opacity(1.0)
            text_clip = text_clip.set_position('center')

            clip_to_overlay = CompositeVideoClip([color_clip, text_clip]).set_duration(end_time - start_time)
            clip_to_overlay = clip_to_overlay.set_position(lambda t: ('center', 100 + t))
            final_clip_overlay = CompositeVideoClip([video_clip, clip_to_overlay])
            clips.append(final_clip_overlay)

        final_clip = concatenate_videoclips(clips)
        clip = final_clip.set_fps(24)

        base_dir = os.getenv("base_dir")

        clip.write_videofile(
            f"{base_dir}/ai/ai_agency_03_video_captions/captioned/{new_file_name}.mp4",
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True)

        return transcript

    except FileNotFoundError as f:
        return f"The specified audio file could not be found: {str(f)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
