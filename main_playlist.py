from __future__ import unicode_literals

import logging

from yt_dlp import YoutubeDL

logger = logging.getLogger(__name__)


def main(input_url):
    yt_opts = {
        "verbose": False,
        # "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
        "format": "136+140,298+140",  # Video format 136 or 298 with audio format 140
        "merge_output_format": "mp4",  # Merge into an MP4 file
        # "format": "bestvideo+bestaudio/best",
        "writeautomaticsub": True,
        "subtitlesformat": "vtt",
        "skip_download": False,
        "outtmpl": "downloads/%(uploader)s/%(playlist_title)s/%(playlist_index)s-%(title)s.%(ext)s",
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
    save_path = "downloads"
    # input_url = input("Enter your URL: ")
    url = "https://youtube.com/playlist?list=PL-2EBeDYMIbSBjHGYJYl1WLUT-tbCLHOb&si=5HAeMnFMtCaq_RIW"
    main(url)
