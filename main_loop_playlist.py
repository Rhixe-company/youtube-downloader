from __future__ import unicode_literals

import logging

from yt_dlp import YoutubeDL

logger = logging.getLogger(__name__)


def main(input_url):
    yt_opts = {
        "verbose": False,
        # "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
        # "format": "bv+ba",
        # "format": "bv[ext=mp4]+ba",
        # "format": "bestvideo+bestaudio/best",
        "format": "136+140,298+140",  # Video format 136 or 298 with audio format 140
        "merge_output_format": "mp4",  # Merge into an MP4 file
        "writeautomaticsub": True,
        "subtitlesformat": "vtt",
        "skip_download": False,
        "outtmpl": "downloads/%(uploader)s/%(playlist_title)s/%(playlist_index)s-%(title)s.%(ext)s",  # %(uploader)s-97ac0bc8/%(upload_date)s__%(id)s.%(ext)s
        "subtitleslangs": ["en"],
        "writethumbnail": True,
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            },
        ],
    }
    msg1 = f"Downloading {input_url}"
    logger.info(msg1)
    with YoutubeDL(yt_opts) as ydl:
        ydl.download([input_url])


if __name__ == "__main__":
    urls = [
        "https://youtu.be/B3DHE9RIimY?si=aaH_-1iXo7MK2nQA",
        # "https://youtu.be/8nh61pOAe8A?si=flUG4fENv4Elpyk8",
        # "https://youtu.be/cUK9nSQuSIA?si=xUg5ITYMI1xxq8MY",
        # "https://youtu.be/9CMvL0oN6tI?si=_B9YK0GXXheLKY1B",
        # "https://youtu.be/BkuxmZeBSRk?si=BuHGFyCiA-kKKM5v",
        # "https://youtu.be/pZSYhei8yPI?si=GNilrqp5LPXZCjeW",
        # "https://youtu.be/5V_APS3l7t0?si=P_sUe7by1Z9FpqH6"
    ]
    for link in urls:
        url = link
        main(url)
    logger.info(f"Done Downloading {urls}")
    # yt-dlp -Uv -N 5 --progress -f bestvideo+bestaudio/best --download-archive archives/archive-97ac0bc8.txt --write-subs --convert-subs srt --merge-output-format=mkv -i --add-metadata --write-annotations --write-info-json --write-thumbnail --write-description -o %(uploader)s-97ac0bc8/%(upload_date)s__%(id)s.%(ext)s --yes-playlist https://www.youtube.com/c/NBNNNewsLaz/videos
