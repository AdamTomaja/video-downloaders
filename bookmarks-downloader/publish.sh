#!/bin/sh

docker build -t vault:5556/bookmarks-downloader .
docker push vault:5556/bookmarks-downloader
