import cv2
import os

video_path = "test_video_no_audio.mp4"
cap = cv2.VideoCapture(video_path)

try:
    if not os.path.exists("screenshots"):
        os.mkdir("screenshots")
except OSError:
    print("Error creating directory of screenshots")

if not cap.isOpened():
    print("Error opening video file: " + video_path)
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
# get frame width and height
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# get total number of frames
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# get duration of video
duration = total_frames / fps
# print video information
print("Video path: " + video_path)
print("FPS: " + str(fps))
print("Width: " + str(width))
print("Height: " + str(height))
print("Total frames: " + str(total_frames))
print("Duration: " + str(duration) + " seconds")

interval = 10
current_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    timestamp = int(current_time)

    if timestamp % interval == 0:
        name = f'screenshots/frame_{timestamp}.jpg'
        cv2.imwrite(name, frame)

    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    current_time += 1 / frame_rate

cap.release()
cv2.destroyAllWindows()
