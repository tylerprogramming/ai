import yt_dlp
import os


class YouTubeAudioDownloader:
    def __init__(self, url, output_template='%(title)s [%(id)s].%(ext)s'):
        self.url = url
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }]
        }

    def download_audio(self):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            info_dict = ydl.extract_info(self.url, download=True)
            filename = ydl.prepare_filename(info_dict)
        return self.find_file_in_directory(filename)

    @staticmethod
    def find_file_in_directory(base_filename):
        base_name, _ = os.path.splitext(base_filename)
        for file in os.listdir('.'):
            if file.startswith(base_name):
                return file
        raise FileNotFoundError(f"The file {base_filename} does not exist in the current directory.")
