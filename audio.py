import os
from yt_dlp import YoutubeDL

def download_audio(youtube_url, output_directory="downloads"):
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Configure yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(output_directory, '%(title)s.%(ext)s'),
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        print(f"Audio downloaded successfully to {output_directory}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    youtube_url = input("Enter the YouTube video URL: ")
    output_dir = input("Enter the output directory (default: downloads): ") or "downloads"
    download_audio(youtube_url, output_dir)

