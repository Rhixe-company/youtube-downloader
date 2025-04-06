from __future__ import unicode_literals

import logging

from yt_dlp import YoutubeDL

logger = logging.getLogger(__name__)


def main(input_url):
    yt_opts = {
        "verbose": False,
        "format": "bv+ba",
        "writeautomaticsub": True,
        "subtitlesformat": "vtt",
        "skip_download": False,
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "subtitleslangs": ["en"],
        "writethumbnail": True,
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mkv",
            },
        ],
    }
    msg = f"Starting {input_url}"
    logger.debug(msg)
    with YoutubeDL(yt_opts) as ydl:
        ydl.download([input_url])
    msg1 = f"Done Downloading {input_url}"
    logger.debug(msg1)


if __name__ == "__main__":
    urls = [
        "https://youtu.be/4VvYOWiQch4?si=S0G5-0PVMBZbAN4Z",
        "https://youtu.be/_q6QlaBakTM?si=1FY4oluHsPind7wB",
        "https://youtu.be/JyIuMooTRFA?si=LS0Zx14aHy23yGzC",
        "https://youtu.be/CpvkCzd2O6A?si=aeAfGbnBLaOg1Tg-",
        "https://youtu.be/PZKH5S0C8EI?si=oOpqchS4Ys8A-nIR",
        "https://youtu.be/Wp6LRijW9wg?si=Amv9_9Wm8_KwPMsK",
        "https://youtu.be/m5dwVl4-GAs?si=iDY7cqNOke71R6yc",
        "https://youtu.be/vBdBB7kM74w?si=Em7CtOVew46v68t4",
        "https://youtu.be/YQuyZLOXDW4?si=3DmikIRKyv6V7u0t",
        "https://youtu.be/UCkRBhfU6zo?si=jc0F3OrnG62cz5RF",
        "https://youtu.be/SDiaKMD1hPA?si=Arv6UW6jLjeB04q5",
        "https://youtu.be/HhCNYt_RWl8?si=ArZxhK5MMQHwxQBL",
    ]
    for link in urls:
        url = link
        main(url)
        logger.debug(f"Done Downloading {url}")
