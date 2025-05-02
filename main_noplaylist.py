from __future__ import unicode_literals

import logging

from yt_dlp import YoutubeDL

logger = logging.getLogger(__name__)


def main(input_url):
    yt_opts = {
        "verbose": False,
       "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
        "writeautomaticsub": True,
        "subtitlesformat": "vtt",
        "skip_download": False,
        "outtmpl": "downloads/%(uploader)s/%(title)s.%(ext)s",
        "subtitleslangs": ["en"],
        "writethumbnail": True,
        # "postprocessors": [
        #     {
        #         "key": "FFmpegVideoConvertor",
        #         "preferedformat": "mp4",
        #     },
        # ],
    }
    msg = f"Starting {input_url}"
    logger.info(msg)
    with YoutubeDL(yt_opts) as ydl:
        ydl.download([input_url])
    msg1 = f"Done Downloading {input_url}"
    logger.info(msg1)


if __name__ == "__main__":
    # input_url = input("Enter your URL: ")
    url = "https://youtu.be/22TkO8og4_Q?si=ercIgmh605bsGm-7"
    main(url)
