import os
from yt_dlp import YoutubeDL
from tqdm import tqdm

def download_playlist():
    # Prompt the user for the playlist URL and download path
    playlist_url = input("Enter the YouTube playlist URL: ").strip()
    download_path = input("Enter the download path: ").strip()

    # Ensure the download path exists
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Set up options for yt-dlp
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(download_path, '%(playlist_index)s - %(title)s.%(ext)s'),
        'ignoreerrors': True,
        'quiet': True,
        'no_warnings': True,
    }

    # Initialize the progress bar
    with YoutubeDL(ydl_opts) as ydl:
        # Extract playlist information
        playlist_dict = ydl.extract_info(playlist_url, download=False)
        video_urls = ['https://www.youtube.com/watch?v=' + entry['id'] for entry in playlist_dict['entries'] if entry]

        # Download videos with progress bar
        for url in tqdm(video_urls, desc='Downloading videos'):
            try:
                ydl.download([url])
            except Exception as e:
                print(f"Error downloading {url}: {e}")

    print("Download completed.")

if __name__ == "__main__":
    download_playlist()
