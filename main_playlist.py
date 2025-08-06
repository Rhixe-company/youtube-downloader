from __future__ import unicode_literals

import logging

from yt_dlp import YoutubeDL

logger = logging.getLogger(__name__)


def main(input_url):
    yt_opts = {
        "verbose": False,
        "format": "136+bestaudio,298+bestaudio,232+bestaudio,612+bestaudio,bestvideo+bestaudio/best",
        # "format": "136+140,298+140",  # Video format 136 or 298 with audio format 140
        "merge_output_format": "mkv",  # Merge into an MKV file
        "writeautomaticsub": True,
        "subtitlesformat": "vtt",
        # "noplaylist": False,  # Set to False to download the entire playlist
        "skip_download": False,
        "outtmpl": "downloads/%(uploader)s/%(playlist_title)s/%(playlist_index)s-%(title)s.%(ext)s",
        "subtitleslangs": ["en"],
        # "writesubtitles": True,
        # "subtitleslangs": "all",
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
    save_path = "downloads"
    # input_url = input("Enter your URL: ")

    url = "https://youtube.com/playlist?list=PLA4JPGpQHctT__mDO9EHvOrWVW0Hkf5Mk&si=p7ls1KcifZ4Phowu"
    main(url)
