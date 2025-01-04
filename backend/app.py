from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from onset_slideshow import create_onset_based_slideshow

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust origins for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Beat-Sync Backend API!"}


@app.get("/health")
def health_check():
    return {"status": "Backend is running!"}


UPLOAD_FOLDER = "media/uploads"
GENERATED_FOLDER = "media/generated_videos"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)


@app.post("/upload")
async def upload_files(
    audio: UploadFile = File(...), images: list[UploadFile] = File(...)
):
    try:
        # Log request start
        print("=== Received a request to process files ===")

        # Save audio file
        audio_path = os.path.join(UPLOAD_FOLDER, audio.filename)
        print(f"Saving audio file to {audio_path}")
        with open(audio_path, "wb") as f:
            f.write(await audio.read())

        # Save image files
        image_folder = os.path.join(UPLOAD_FOLDER, "images")
        os.makedirs(image_folder, exist_ok=True)
        print(f"Saving images to {image_folder}")

        image_paths = []
        for img in images:
            image_path = os.path.join(image_folder, img.filename)
            print(f"Saving image: {image_path}")
            with open(image_path, "wb") as f:
                f.write(await img.read())
            image_paths.append(image_path)

        # Log video generation start
        print("=== Starting video generation process ===")
        output_video_path = os.path.join(GENERATED_FOLDER, "generated_slideshow.mp4")
        create_onset_based_slideshow(audio_path, image_folder, output_video_path)
        print(f"Video generated successfully at {output_video_path}")

        # Cleanup temporary files
        print("Cleaning up temporary files...")
        shutil.rmtree(image_folder)
        os.remove(audio_path)
        print("Temporary files cleaned up.")

        # Log success and return response
        print("=== Request completed successfully ===")
        return FileResponse(
            output_video_path,
            media_type="video/mp4",
            filename="generated_slideshow.mp4",
        )

    except Exception as e:
        # Log error
        print(f"Error occurred: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/health")
def health_check():
    return {"status": "Backend is running!"}
