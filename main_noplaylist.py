from __future__ import unicode_literals

import logging

from yt_dlp import YoutubeDL

logger = logging.getLogger(__name__)


def main(input_url):
    yt_opts = {
        "verbose": True,
        "format": "136+ba,298+ba,232+ba,bv+ba",  # Video format 136 or 298 with audio format 140
        "merge_output_format": "mkv",  # Merge into an MKV file
        "writeautomaticsub": True,
        "subtitlesformat": "srt",
        "noplaylist": True,  # Set to False to download the entire playlist
        "skip_download": False,
        "outtmpl": "downloads/%(uploader)s/%(title)s.%(ext)s",
        "subtitleslangs": ["en"],
        "writesubtitles": True,
        "writethumbnail": True,
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mkv",
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
    url = "https://youtu.be/Zq5fmkH0T78?si=2PhOrKyGWqTUJrVo"
    main(url)
