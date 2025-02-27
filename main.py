from __future__ import unicode_literals

import logging

import yt_dlp

# from yt_dlp.utils import download_range_func  # noqa: F401


logger = logging.getLogger(__name__)


def main(input_url, save_path):
    # start_time = 2  # accepts decimal value like 2.3
    # end_time = 7

    yt_opts = {
        "verbose": True,
        # "download_ranges": download_range_func(None, [(start_time, end_time)]),
        # "force_keyframes_at_cuts": True,
        # "format": "bestvideo+bestaudio/best",
        "format": "bestvideo*+bestaudio/best",
        "writeautomaticsub": True,
        "subtitlesformat": "srt",
        # "writesubtitles": True,
        # "allsubtitles": True,
        "skip_download": False,
        "outtmpl": save_path + "/%(playlist_index)s-%(title)s.%(ext)s",
        "subtitleslangs": ["en"],
        # "subtitleslangs": ["en", "fr"],
        "postprocessors": [
            # {
            #     "key": "FFmpegMetadata",
            # },
            # {
            #     "key": "EmbedThumbnail",
            #     "already_have_thumbnail": True,  # overwrite any thumbnails already present
            # },
            {
                "key": "FFmpegInputConvertor",
                "preferedformat": "mp4",
            },
        ],
    }
    with yt_dlp.YoutubeDL(yt_opts) as ydl:
        ydl.download([input_url])
    msg1 = f"Done Downloading {input_url}"
    logger.info(msg1)


if __name__ == "__main__":
    save_path = "downloads/Django REST Framework"
    input_url = input("Enter your URL: ")
    # url = "https://youtube.com/playlist?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t&si=gF6wqVQf4vtWZ5d0"
    msg = f"Starting {input_url}"
    logger.info(msg)
    main(input_url, save_path)
