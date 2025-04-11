from __future__ import unicode_literals

import logging

from yt_dlp import YoutubeDL

logger = logging.getLogger(__name__)


def main(input_url):
    yt_opts = {
        "verbose": False,
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
        # "format": "bv+ba",
        "writeautomaticsub": True,
        "subtitlesformat": "vtt",
        "skip_download": False,
        "outtmpl": "downloads/%(uploader)s/%(title)s.%(ext)s",  # %(uploader)s-97ac0bc8/%(upload_date)s__%(id)s.%(ext)s
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
    logger.debug(msg1)
    with YoutubeDL(yt_opts) as ydl:
        ydl.download([input_url])


if __name__ == "__main__":
    urls = [
        # "https://youtu.be/ZJr7mmaEXiE?si=qhAXq4E50yhysvrh",
        # "https://youtu.be/beVGYjMSRRk?si=6dxG4tqL49t1j7fK",
        "https://youtu.be/lc1sOvRaFpg?si=IVvhHtii21ZNlZA_",
        "https://youtu.be/PgHaH8tGdWw?si=Z4xPiwMl6QO1PN4Z",
        "https://youtu.be/Pc96-4_gqJ4?si=fVywee_x83PyCZba",
    ]
    for link in urls:
        url = link
        main(url)
    logger.debug(f"Done Downloading {urls}")
    # yt-dlp -Uv -N 5 --progress -f bestvideo+bestaudio/best --download-archive archives/archive-97ac0bc8.txt --write-subs --convert-subs srt --merge-output-format=mkv -i --add-metadata --write-annotations --write-info-json --write-thumbnail --write-description -o %(uploader)s-97ac0bc8/%(upload_date)s__%(id)s.%(ext)s --yes-playlist https://www.youtube.com/c/NBNNNewsLaz/videos
