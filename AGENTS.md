# youtube-downloader

## Architecture
- **Type:** Python CLI downloader for YouTube
- **Pattern:** Single-file scripts with yt-dlp + curl_cffi; supports single video, playlist, and loop modes
- **Reference:** [Workflow Analysis](docs/Project_Architecture/Workflow_Analysis.md), [Exemplars](docs/Project_Architecture/exemplars.md)

Python 3.x CLI tool using yt-dlp + curl_cffi for YouTube content downloading. Supports single video, playlist, and loop/ batch modes.

## Stack
- **Language:** Python 3.x
- **Key Libraries:** `yt-dlp`, `curl_cffi`
- **Quality:** `ruff` (lint), `mypy` (type check, optional)
- **External Deps:** FFmpeg (for post-processing/conversions)

## Commands
```bash
pip install yt-dlp curl_cffi
python main_noplaylist.py          # single video
python main_playlist.py            # playlist
python main_loop_playlist.py       # batch loop mode
python test.py                     # run tests
ruff check . && mypy *.py          # optional lint/type-check
```

## Conventions
- Single CLI tool — no web deployment or framework
- `.env` / URLs — never commit
- Keep yt-dlp updated for site compatibility
- FFmpeg required for format conversions
- Add delays between requests to respect rate limits
- `ruff` for linting; `mypy` type hints optional

## Notes
- No web UI or API — pure CLI
- curl_cffi for bypassing some bot protections
- Loop mode for bulk/batch processing
- Test via `python test.py`
