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
        "noplaylist": False,  # Set to False to download the entire playlist
        "skip_download": False,
        "outtmpl": "downloads/%(uploader)s/%(playlist_title)s/%(playlist_index)s-%(title)s.%(ext)s",
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
    save_path = "downloads"
    # input_url = input("Enter your URL: ")

    url = "https://youtube.com/playlist?list=PLGk7ftfMz7jbF-vCLxaE0-zrW_gj6V9YG&si=kTFeecP7eKiSaCl0"
    main(url)
