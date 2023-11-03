import cv2
import os
import subprocess
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()


# Define a model for response
class VideoInfo(BaseModel):
    fps: float
    width: int
    height: int
    total_frames: int
    duration: float


# Directory to store videos and screenshots
video_dir = "video_dir"
screenshot_dir = "screenshot_dir"
os.makedirs(video_dir, exist_ok=True)
os.makedirs(screenshot_dir, exist_ok=True)


# Function to remove audio from video
def remove_audio(input_file, output_file):
    print("Removing audio from video file: " + input_file)
    command = f'ffmpeg -i {input_file} -an -c:v copy {output_file}'
    print("Running command: " + command)
    subprocess.run(command, shell=True, check=True)
    print("completed")


# Function to capture screenshots
def capture_screenshots(video_path, interval):
    cap = cv2.VideoCapture(video_path)
    screenshots = []

    if not cap.isOpened():
        return screenshots

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    current_time = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        timestamp = int(current_time)

        if timestamp % interval == 0:
            name = f'{screenshot_dir}/frame_{timestamp}.jpg'
            cv2.imwrite(name, frame)
            screenshots.append(name)

        frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
        current_time += 1 / frame_rate

    cap.release()
    cv2.destroyAllWindows()
    return screenshots


# API route to upload a video file, remove audio, capture screenshots, and get video info
@app.post("/process_video/")
async def process_video(
        video_file: UploadFile = File(...),
        interval: int = Form(...),
):
    # Save the video file
    video_path = os.path.join(video_dir, video_file.filename)
    with open(video_path, "wb") as f:
        f.write(video_file.file.read())

    # Remove audio from video
    video_without_audio_path = os.path.join(video_dir, "video_no_audio.mp4")
    remove_audio(video_path, video_without_audio_path)

    # Capture screenshots
    screenshots = capture_screenshots(video_path, interval)

    # Get video information
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    cap.release()

    video_info = VideoInfo(fps=fps, width=width, height=height, total_frames=total_frames, duration=duration)

    return {
        "video_info": video_info,
        "screenshots": screenshots,
    }
