import os
import subprocess
import librosa
import numpy as np


def detect_onsets(audio_file):
    """
    Detect onsets in the audio file using Librosa.
    """
    print(f"Detecting onsets for {audio_file}...")
    y, sr = librosa.load(audio_file, sr=None)
    onset_env = librosa.onset.onset_strength(
        y=y, sr=sr, hop_length=512, aggregate=np.median
    )
    onsets = librosa.onset.onset_detect(
        onset_envelope=onset_env, sr=sr, hop_length=512, units="time"
    )
    print(f"Detected onsets: {onsets}")
    return onsets, sr


def create_image_sequence_from_onsets(images_folder, onsets, audio_length, output_dir):
    """
    Create image sequences based on detected onsets for slideshow transitions.
    """
    os.makedirs(output_dir, exist_ok=True)
    images = sorted(
        [
            os.path.join(images_folder, img)
            for img in os.listdir(images_folder)
            if img.endswith((".png", ".jpg"))
        ]
    )
    if not images:
        raise ValueError(f"No images found in {images_folder}.")

    image_sequence = []
    onsets = [0] + list(onsets) + [audio_length]  # Include start and end of audio
    num_images = len(images)

    ffmpeg_input = os.path.join(output_dir, "ffmpeg_input.txt")
    with open(ffmpeg_input, "w") as f:
        for i in range(len(onsets) - 1):
            image_path = images[
                i % num_images
            ]  # Loop through images if fewer than onsets
            duration = onsets[i + 1] - onsets[i]
            f.write(f"file '{os.path.abspath(image_path)}'\n")
            f.write(f"duration {duration}\n")

        # Repeat the last frame to ensure audio length matches video
        f.write(f"file '{os.path.abspath(images[-1])}'\n")

    return ffmpeg_input


def create_video_from_images(ffmpeg_input, audio_file, output_file):
    """
    Combine images into a video and add audio using FFmpeg.
    """
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        ffmpeg_input,
        "-i",
        audio_file,
        "-map",
        "0:v",
        "-map",
        "1:a",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-strict",
        "experimental",
        "-shortest",
        output_file,
    ]
    print(f"Running FFmpeg command: {' '.join(ffmpeg_cmd)}")
    subprocess.run(ffmpeg_cmd, check=True)


def create_onset_based_slideshow(audio_file, images_folder):
    """
    Create a slideshow video synchronized with audio onsets.
    """
    # Step 1: Detect onsets
    onsets, sr = detect_onsets(audio_file)

    # Step 2: Get audio length
    y, sr = librosa.load(audio_file, sr=None)
    audio_length = len(y) / sr

    # Step 3: Create image sequence
    output_dir = "onset_frames"
    ffmpeg_input = create_image_sequence_from_onsets(
        images_folder, onsets, audio_length, output_dir
    )

    # Step 4: Generate video
    create_video_from_images(ffmpeg_input, audio_file, "onset_slideshow7.mp4")

    print("Onset-based slideshow created successfully!")


# Example Usage
if __name__ == "__main__":
    audio_file = "audio7.mp3"
    images_folder = "images"
    create_onset_based_slideshow(audio_file, images_folder)
