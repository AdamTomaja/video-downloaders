FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the script to the working directory
COPY script.py .

RUN mkdir /output

# Install yt-dlp
RUN apt-get update && apt-get install -y curl ffmpeg && \
    curl -L https://github.com/yt-dlp/yt-dlp/releases/download/2023.06.22/yt-dlp -o /usr/bin/yt-dlp && \
    chmod a+rx /usr/bin/yt-dlp

RUN pip install requests 
    

# Set environment variables
ENV BOOKMARKS_URL=""
ENV DOWNLOAD_PARAMETERS=""
ENV SLEEP_TIME=""

# Run the script
CMD python script.py
