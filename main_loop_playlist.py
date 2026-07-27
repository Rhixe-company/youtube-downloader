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
        "outtmpl": "downloads/%(uploader)s/%(playlist_title)s/%(playlist_index)s-%(title)s.%(ext)s",  # %(uploader)s-97ac0bc8/%(upload_date)s__%(id)s.%(ext)s
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
    urls = [
        "https://youtu.be/FTH6Dn3AyIQ?si=7w_dVuT9JdZKgG0t",
        "https://youtu.be/PuOVqP_cjkE?si=7ljitzZHygeg3A95",
        "https://youtu.be/xZ1ba-RLrjo?si=6whLrlsvtYv9HPL2",
    ]
    for link in urls:
        url = link
        main(url)
    logger.info(f"Done Downloading {urls}")
    # yt-dlp -Uv -N 5 --progress -f bestvideo+bestaudio/best --download-archive archives/archive-97ac0bc8.txt --write-subs --convert-subs srt --merge-output-format=mkv -i --add-metadata --write-annotations --write-info-json --write-thumbnail --write-description -o %(uploader)s-97ac0bc8/%(upload_date)s__%(id)s.%(ext)s --yes-playlist https://www.youtube.com/c/NBNNNewsLaz/videos
