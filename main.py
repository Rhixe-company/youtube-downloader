from __future__ import unicode_literals

import logging

from yt_dlp import YoutubeDL

logger = logging.getLogger(__name__)


def main(input_url, save_path):
    yt_opts = {
        "verbose": True,
        "format": "bestvideo*+bestaudio/best",
        "writeautomaticsub": True,
        "subtitlesformat": "vtt",
        "skip_download": False,
        "outtmpl": save_path
        + "/%(playlist_title)s/%(playlist_index)s-%(title)s.%(ext)s",
        "subtitleslangs": ["en"],
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
    save_path = "downloads"
    input_url = input("Enter your URL: ")
    # url = "https://youtube.com/playlist?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t&si=gF6wqVQf4vtWZ5d0"
    main(input_url, save_path)
