from __future__ import unicode_literals

import logging

from yt_dlp import YoutubeDL

logger = logging.getLogger(__name__)


def main(input_url):
    yt_opts = {
        "verbose": False,
        # "format": "bestvideo+bestaudio/best",
        "format": "136+140,298+140",  # Video format 136 or 298 with audio format 140
        "merge_output_format": "mp4",  # Merge into an MP4 file
        "writeautomaticsub": True,
        "subtitlesformat": "vtt",
        "skip_download": False,
        "outtmpl": "downloads/%(uploader)s/%(title)s.%(ext)s",
        "subtitleslangs": ["en"],
        "writethumbnail": True,
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            },
        ],
    }
    msg = f"Starting {input_url}"
    logger.info(msg)
    with YoutubeDL(yt_opts) as ydl:
        ydl.download([input_url])
    msg1 = f"Done Downloading {input_url}"
    logger.info(msg1)


if __name__ == "__main__":
    # input_url = input("Enter your URL: ")
    url = "https://youtu.be/g0EgwfQJew8?si=ApQZXGpU9NmPCvK3"
    main(url)
