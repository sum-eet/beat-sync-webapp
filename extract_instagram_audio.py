import os
import subprocess
from yt_dlp import YoutubeDL


def extract_audio_from_instagram(instagram_url, output_dir="downloads"):
    """
    Extract audio from an Instagram video link and save it as an MP3.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_template = os.path.join(output_dir, "audio.%(ext)s")

    # Configure yt-dlp options
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    try:
        # Use yt-dlp to download and extract audio
        with YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading and extracting audio from {instagram_url}...")
            ydl.download([instagram_url])
            print("Audio extracted successfully!")
            return os.path.join(output_dir, "audio.mp3")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Test the function
if __name__ == "__main__":
    instagram_link = input("Enter an Instagram video URL: ")
    audio_file = extract_audio_from_instagram(instagram_link)
    if audio_file:
        print(f"Audio saved at: {audio_file}")
    else:
        print("Failed to extract audio.")
