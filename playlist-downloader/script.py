#!/usr/bin/env python3

import subprocess
import time
import logging
import os
import json

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

playlist_url = os.environ.get("PLAYLIST_URL", "")
download_parameters = os.environ.get("DOWNLOAD_PARAMETERS", "")

if not playlist_url:
    logger.error("Playlist URL is not set.")
    exit(1)


download_command = f"yt-dlp {download_parameters} https://youtube.com/watch?v="


# Command to retrieve video IDs from the playlist
id_command = f"yt-dlp --get-id --flat-playlist {playlist_url}"

# Set the monitoring interval
monitoring_interval = 60  # seconds

processed_videos_file = "/output/processed_videos.json"


# Keep track of the processed video IDs
processed_videos = set()

if os.path.isfile(processed_videos_file):
    with open(processed_videos_file, "r") as file:
        processed_videos = set(json.load(file))

while True:
    # Get the video IDs from the playlist
    try:
        video_ids = subprocess.check_output(id_command, shell=True, text=True).splitlines()
    except subprocess.CalledProcessError as e:
        logger.error("Error retrieving video IDs: %s", e)
        continue

    # Process new videos
    for video_id in video_ids:
        if video_id not in processed_videos:
            # Download the video as MP3
            download_url = f"{download_command}{video_id}"
            try:
                subprocess.run(download_url, shell=True, check=True)
                logger.info("Downloaded video with ID: %s", video_id)
                processed_videos.add(video_id)
                 # Save the processed videos to file
                with open(processed_videos_file, "w") as file:
                    json.dump(list(processed_videos), file)
            except subprocess.CalledProcessError as e:
                logger.error("Error downloading video with ID %s: %s", video_id, e)

    # Wait for the next monitoring interval
    logger.info("Waiting %d seconds for the next iteration...", monitoring_interval)
    time.sleep(monitoring_interval)
