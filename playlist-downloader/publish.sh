#!/bin/sh

docker build -t vault:5556/yt-playlist-downloader .
docker push vault:5556/yt-playlist-downloader
