import subprocess

input_file = "test_video.mp4"
output_file = "test_video_no_audio.mp4"

# ffmpeg command to remove audio from video file

command = f'ffmpeg -i {input_file} -an -c:v copy {output_file}'

try:
    subprocess.run(command, shell=True, check=True)
    print("Audio removed from video file: " + input_file)
except subprocess.CalledProcessError as e:
    print("Error: " + str(e))
    exit(1)
