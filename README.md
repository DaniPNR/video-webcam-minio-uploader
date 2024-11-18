# video-webcam-minio-uploader
Video Webcam MinIO Uploader This Python project captures video segments from a webcam, encodes them using FFmpeg, saves them locally, and uploads them to a MinIO bucket. 
It includes features like automatic segmentation, deletion of local files after upload, and configurable video parameters.

# Video Webcam MinIO Uploader

This project captures video from a webcam, saves it locally in MP4 format, and uploads it to a MinIO bucket.

## Features
- Webcam recording with FFmpeg
- Automatic video segmentation and upload to MinIO
- Deletes local files after successful upload

## Prerequisites
- Python 3.x
- MinIO server running locally or remotely
- FFmpeg installed

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/DaniPNR/video-webcam-minio-uploader.git
   cd video-webcam-minio-uploader

