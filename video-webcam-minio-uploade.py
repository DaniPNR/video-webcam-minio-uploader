import cv2
import subprocess
import time
import os
import datetime
from minio import Minio

# Initialize MinIO client
minio_client = Minio(
    "localhost:9000",
    access_key="danipnr",
    secret_key="danipnr123",
    secure=False,
)

# Check or create bucket
bucket_name = "video-storagewebcam"
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)

# Camera settings
camera_index = 1
cap = cv2.VideoCapture(camera_index)
if not cap.isOpened():
    print("Camera could not be opened. Exiting.")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

# Video output settings
camera_identifier = "192_168_1_1".replace(".", "_")  # Replace dots in IP with underscores
output_directory = "D:/videos_minio/"
os.makedirs(output_directory, exist_ok=True)
segment_duration = 60
frame_rate = 30
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

try:
    while True:
        # Current date and time for naming
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{output_directory}{camera_identifier}_{current_time}.mp4"

        # Start FFmpeg process
        ffmpeg_command = [
            "ffmpeg",
            "-y",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-pix_fmt", "bgr24",
            "-s", f"{frame_width}x{frame_height}",
            "-r", str(frame_rate),
            "-i", "-",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            output_file,
        ]
        ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

        start_time = time.time()
        while time.time() - start_time < segment_duration:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame.")
                break
            ffmpeg_process.stdin.write(frame.tobytes())

        ffmpeg_process.stdin.close()
        ffmpeg_process.wait()

        # Check and upload video
        if os.path.exists(output_file):
            object_name = f"{camera_identifier}/{current_time}.mp4"  # Folder structure in MinIO
            minio_client.fput_object(bucket_name, object_name, output_file)
            print(f"Uploaded {object_name} to MinIO.")
            os.remove(output_file)  # Delete the file after successful upload
            print(f"Deleted local file: {output_file}")
        else:
            print(f"File {output_file} not found, skipping upload.")

except KeyboardInterrupt:
    print("Recording stopped.")

finally:
    cap.release()
    print("Webcam released.")
