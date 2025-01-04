import os
import subprocess
import librosa
import numpy as np
from PIL import Image


def preprocess_images(images_folder):
    """
    Resize images to a smaller resolution and ensure dimensions are divisible by 2.
    """
    max_resolution = 800  # Max width/height for images
    for img_file in os.listdir(images_folder):
        if img_file.endswith((".png", ".jpg", ".jpeg")):
            img_path = os.path.join(images_folder, img_file)
            with Image.open(img_path) as img:
                # Resize image while maintaining aspect ratio
                img.thumbnail((max_resolution, max_resolution), Image.ANTIALIAS)
                width, height = img.size

                # Ensure dimensions are divisible by 2
                new_width = width if width % 2 == 0 else width - 1
                new_height = height if height % 2 == 0 else height - 1
                img = img.resize((new_width, new_height))
                img.save(img_path)


def detect_onsets(audio_file):
    y, sr = librosa.load(audio_file, sr=None)
    onset_env = librosa.onset.onset_strength(
        y=y, sr=sr, hop_length=512, aggregate=np.median
    )
    onsets = librosa.onset.onset_detect(
        onset_envelope=onset_env, sr=sr, hop_length=512, units="time"
    )
    return onsets, sr


def create_image_sequence_from_onsets(images_folder, onsets, audio_length, output_dir):
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
            image_path = images[i % num_images]
            duration = onsets[i + 1] - onsets[i]
            f.write(f"file '{os.path.abspath(image_path)}'\n")
            f.write(f"duration {duration}\n")

        f.write(f"file '{os.path.abspath(images[-1])}'\n")

    return ffmpeg_input


def create_video_without_audio(ffmpeg_input, output_video_path):
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        ffmpeg_input,
        "-vf",
        "scale=trunc(iw/2)*2:trunc(ih/2)*2",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        output_video_path,
    ]
    subprocess.run(ffmpeg_cmd, check=True)


def add_audio_to_video(video_path, audio_file, output_file):
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,
        "-i",
        audio_file,
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-strict",
        "experimental",
        "-shortest",
        output_file,
    ]
    subprocess.run(ffmpeg_cmd, check=True)


def create_onset_based_slideshow(audio_file, images_folder, output_path):
    preprocess_images(images_folder)

    onsets, sr = detect_onsets(audio_file)
    y, sr = librosa.load(audio_file, sr=None)
    audio_length = len(y) / sr
    output_dir = os.path.join(os.path.dirname(output_path), "onset_frames")
    ffmpeg_input = create_image_sequence_from_onsets(
        images_folder, onsets, audio_length, output_dir
    )
    video_no_audio = "media/generated_videos/video_no_audio.mp4"
    final_video = "media/generated_videos/generated_slideshow.mp4"

    create_video_without_audio(ffmpeg_input, video_no_audio)
    add_audio_to_video(video_no_audio, audio_file, output_path)

    return output_path
