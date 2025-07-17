from __future__ import unicode_literals

import logging

from yt_dlp import YoutubeDL

logger = logging.getLogger(__name__)


def main(input_url):
    yt_opts = {
        "verbose": False,
        "format": "136+bestaudio,298+bestaudio,232+bestaudio,612+bestaudio",  # Video format 136 or 298 with audio format 140
        "merge_output_format": "mkv",  # Merge into an MKV file
        "writeautomaticsub": True,
        "subtitlesformat": "vtt",
        "skip_download": False,
        "outtmpl": "downloads/%(uploader)s/%(title)s.%(ext)s",  # %(uploader)s-97ac0bc8/%(upload_date)s__%(id)s.%(ext)s
        "subtitleslangs": ["en"],
        "writethumbnail": True,
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mkv",
            },
        ],
    }
    msg1 = f"Downloading {input_url}"
    logger.info(msg1)
    with YoutubeDL(yt_opts) as ydl:
        ydl.download([input_url])


if __name__ == "__main__":
    urls = [
        "https://www.youtube.com/watch?v=0NTUIdUljwM",
        # "https://youtu.be/z-ROjham50M?si=URQaE30w-fdnDAKr",
    ]
    for link in urls:
        url = link
        main(url)
    logger.info(f"Done Downloading {urls}")
    # yt-dlp -Uv -N 5 --progress -f bestvideo+bestaudio/best --download-archive archives/archive-97ac0bc8.txt --write-subs --convert-subs srt --merge-output-format=mkv -i --add-metadata --write-annotations --write-info-json --write-thumbnail --write-description -o %(uploader)s-97ac0bc8/%(upload_date)s__%(id)s.%(ext)s --yes-playlist https://www.youtube.com/c/NBNNNewsLaz/videos
