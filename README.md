# youtube-downloader — CLI Video Downloader

> **Stack:** Python 3.x + yt-dlp | **Type:** CLI Utility Tool | **Status:** Active

A Python CLI tool for downloading YouTube videos (single, playlist, and loop mode) using yt-dlp and curl_cffi. Designed for simplicity with no web deployment.

---

## Technology Stack

| Category | Technology |
| --- | --- |
| **Runtime** | Python ^3.x |
| **Language** | Python |
| **Download Engine** | yt-dlp (latest) |
| **HTTP Client** | curl_cffi (latest) |
| **Media Processing** | FFmpeg (external) |
| **Linting** | ruff (optional) |
| **Type Checking** | mypy (optional) |

## Architecture

```
User Command → Python Script
                    ↓
          ┌─────────┴─────────┐
          ↓         ↓         ↓
    Single Video  Playlist   Loop Mode
          ↓         ↓         ↓
          └─────────┬─────────┘
                    ↓
              yt-dlp API
                    ↓
        ┌───────────┴───────────┐
        ↓                       ↓
    HTTP Request           Rate Limiting
    (curl_cffi)            (Polite Delays)
        ↓                       ↓
    Video/Audio Download   FFmpeg Conversion
        ↓                       ↓
    ┌───────────┬───────────────┘
    ↓           ↓
Output File  Console Progress
```

## Project Structure

```
youtube-downloader/
├── main_noplaylist.py        # Single video download
├── main_playlist.py          # Playlist download
├── main_loop_playlist.py     # Batch loop mode
├── test.py                   # Basic test script
├── requirements/
│   └── base.txt              # Base dependencies
├── .env.example              # Environment template
└── docs/Project_Architecture/
```

## Getting Started

```bash
# Prerequisites: Python 3.x, FFmpeg installed

# Install dependencies
pip install yt-dlp curl_cffi
# Or: pip install -r requirements/base.txt

# Download a single video
python main_noplaylist.py

# Download a playlist
python main_playlist.py

# Batch loop download
python main_loop_playlist.py

# Run basic test
python test.py

# Optional: lint and type check
ruff check .
mypy *.py
```

## Key Features

- **Single Video Download** — Download individual YouTube videos
- **Playlist Download** — Download entire YouTube playlists
- **Loop Mode** — Batch loop mode for continuous playlist downloads
- **yt-dlp Engine** — Active fork of youtube-dl with more features
- **curl_cffi** — Advanced HTTP fingerprinting for reliability
- **FFmpeg Integration** — Format conversion and audio extraction
- **Rate Limiting** — Built-in polite delays

## Scripts Overview

| Script | Purpose |
| --- | --- |
| `main_noplaylist.py` | Download a single video |
| `main_playlist.py` | Download an entire playlist |
| `main_loop_playlist.py` | Batch loop mode for continuous downloading |
| `test.py` | Basic functionality test |

## Coding Standards

- **PEP 8**: Python style guide
- **snake_case**: Variable and function naming
- **Type hints**: Optional type annotations (mypy compatible)
- **Try/except**: Robust error handling for network/download failures
- **Clear purpose**: Each script has a distinct, well-defined purpose

## Usage Tips

- Keep yt-dlp updated for continued functionality: `pip install -U yt-dlp`
- FFmpeg is required for audio extraction and format conversion
- Add delays to respect YouTube rate limits
- If downloads fail, update yt-dlp first

## Security

- No URLs committed to VCS
- `.env` never committed
- Validate URLs to prevent SSRF attacks
- Respect YouTube Terms of Service
- No mass or commercial use
- Scan downloaded files for malware

## Dependencies

| Library | Purpose |
| --- | --- |
| **yt-dlp** | YouTube downloading (active fork of youtube-dl) |
| **curl_cffi** | Advanced HTTP fingerprinting for avoiding detection |

## License

Not specified.
