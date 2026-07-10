# Copilot Instructions

Project-wide guidance for the YouTube downloader CLI.

## Source of truth

- `projects/youtube-downloader/AGENTS.md`
- `README.md`
- `main_*.py`
- `test.py`

## Commands

Run from the project root:

```bash
pip install yt-dlp curl_cffi
pip install -r requirements/base.txt
pip install -r requirements/local.txt
python main_noplaylist.py
python main_playlist.py
python main_loop_noplaylist.py
python main_loop_playlist.py
python test.py
mypy *.py
ruff check .
```

## Architecture

- Python CLI scripts wrap yt-dlp downloads for single videos, playlists, and loops.
- The project is script-oriented, not a web service.
- Support files and docs back the CLI behavior.

## Conventions

- Keep filenames and script names aligned with the mode they implement.
- Validate URLs before download-related work.
- Use polite scraping/download delays and keep yt-dlp current.
- Treat network and filesystem failures as expected runtime conditions.
