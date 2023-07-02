import requests
import subprocess
import os
import json
import time
import logging

BOOKMARKS_URL = os.environ.get("BOOKMARKS_URL", "")
SLEEP_TIME = int(os.environ.get("SLEEP_TIME", "10"))
DOWNLOAD_PARAMETERS = os.environ.get("DOWNLOAD_PARAMETERS", "")

DOWNLOADED_IDS_FILE = '/output/downloaded_ids.json'

download_command = f"yt-dlp {DOWNLOAD_PARAMETERS}"


# Set up logging
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def load_downloaded_ids():
    if not os.path.exists(DOWNLOADED_IDS_FILE):
        logger.info('No existing downloaded bookmarks file found. Creating new.')
        return set()
    with open(DOWNLOADED_IDS_FILE, 'r') as f:
        logger.info('Loaded downloaded bookmark IDs from file.')
        return set(json.load(f))

def save_downloaded_ids(downloaded_ids):
    with open(DOWNLOADED_IDS_FILE, 'w') as f:
        json.dump(list(downloaded_ids), f)
    logger.info('Saved downloaded bookmark IDs to file.')

def download_bookmark(url):
    download_command_with_url = f"{download_command} {url}"
    logger.info(f"Running command: {download_command_with_url}")
    
    subprocess.run(download_command_with_url, shell=True, check=True)

def main():
    logger.info('Starting bookmark monitor.')
    while True:
        logger.info('Checking for new bookmarks.')
        try:
            response = requests.get(BOOKMARKS_URL)
            response.raise_for_status()
        except Exception as e:
            logger.error('Failed to fetch bookmarks: %s', str(e))
            continue

        bookmarks = response.json()['data']

        downloaded_ids = load_downloaded_ids()

        for bookmark in bookmarks:
            if bookmark['id'] not in downloaded_ids:
                logger.info('New bookmark found. ID: %s, URL: %s', bookmark['id'], bookmark['url'])
                try:
                    download_bookmark(bookmark['url'])
                    logger.info('Successfully downloaded bookmark. ID: %s, URL: %s', bookmark['id'], bookmark['url'])
                    downloaded_ids.add(bookmark['id'])
                except subprocess.CalledProcessError:
                    logger.error('Failed to download bookmark. ID: %s, URL: %s', bookmark['id'], bookmark['url'])
                except Exception as e:
                    logger.error('An unexpected error occurred: %s', str(e))

        save_downloaded_ids(downloaded_ids)
        logger.info('Sleeping for %s seconds', SLEEP_TIME)
        time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    main()
