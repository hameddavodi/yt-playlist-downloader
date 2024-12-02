import os
import sys
from yt_dlp import YoutubeDL
from tqdm import tqdm

def download_playlist():
    # Prompt the user for the playlist URL and download path
    playlist_url = input("Enter the YouTube playlist URL: ").strip()
    download_path = input("Enter the download path: ").strip()
    
    # Ensure the download path exists
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    # Set up comprehensive options for yt-dlp
    ydl_opts = {
        # Prefer high-quality MP4 videos with good audio
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        
        # Custom output template to organize playlist downloads
        'outtmpl': os.path.join(download_path, '%(playlist_index)s - %(title)s.%(ext)s'),
        
        # Merge video and audio into a single file
        'merge_output_format': 'mp4',
        
        # Error handling and logging
        'ignoreerrors': True,
        'no_warnings': True,
        
        # Metadata and thumbnail options
        'writeinfojson': True,
        'writethumbnail': True,
        
        # Progress tracking
        'progress_hooks': [create_progress_hook()],
    }
    
    # Initialize YoutubeDL with the options
    with YoutubeDL(ydl_opts) as ydl:
        try:
            # Extract playlist information
            playlist_info = ydl.extract_info(playlist_url, download=False)
            
            # Validate playlist
            if 'entries' not in playlist_info or not playlist_info['entries']:
                print("Error: No videos found in the playlist.")
                return
            
            # Filter out None entries
            video_urls = [
                f"https://www.youtube.com/watch?v={entry['id']}" 
                for entry in playlist_info['entries'] 
                if entry is not None
            ]
            
            # Print playlist information
            print(f"Playlist: {playlist_info.get('title', 'Untitled')}")
            print(f"Total Videos: {len(video_urls)}")
            
            # Download videos
            for url in tqdm(video_urls, desc='Downloading videos', unit='video'):
                try:
                    ydl.download([url])
                except Exception as e:
                    print(f"Error downloading {url}: {e}")
            
            print("Download completed successfully.")
        
        except Exception as e:
            print(f"An error occurred while processing the playlist: {e}")

def create_progress_hook():
    """Create a progress hook for more detailed download tracking."""
    def hook(d):
        if d['status'] == 'finished':
            print('\nDownload complete. Converting...')
        elif d['status'] == 'downloading':
            downloaded_bytes = d.get('downloaded_bytes', 0)
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            if total_bytes > 0:
                percent = downloaded_bytes * 100. / total_bytes
                print(f'\rDownloading: {percent:.1f}%', end='', flush=True)
    return hook

def main():
    try:
        download_playlist()
    except KeyboardInterrupt:
        print("\nDownload interrupted by user.")
        sys.exit(1)

if __name__ == "__main__":
    main()
