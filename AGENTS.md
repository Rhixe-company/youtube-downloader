# AGENTS.md

> **Refreshed by AGENTS workflow 2026-06-01**

## Project Overview

A Python-based YouTube video downloader with playlist support and continuous loop mode. Uses yt-dlp for download operations with curl_cffi support for improved compatibility.

**Tech Stack:**
- **Language**: Python 3.x
- **Download Engine**: yt-dlp with curl_cffi
- **Quality**: Multiple quality options (720p, 1080p, etc.)
- **Features**: Single video download, playlist download, loop mode for batch processing
- **Testing**: Built-in test.py
- **Dev Tools**: djlint (HTML template linting), Faker (test data), pre-commit hooks
- **Docs**: Sphinx documentation (docutils, alabaster theme)

## Hermes and Copilot

- Use the nearest `AGENTS.md` for files under `projects/youtube-downloader/`;
  this file is the local fallback.
- `projects/youtube-downloader/.github/copilot-instructions.md` is the primary
  Copilot guidance file for this project.
- Root Hermes orchestration assets live in `../../.github/agents/hermes.agent.md`
  and `../../.github/prompts/`.
- Keep this file, the local Copilot instructions, and the downloader scripts in
  sync when URL validation, loop mode, or quality options change.

## Setup Commands

```bash
# Install production dependencies
pip install yt-dlp curl_cffi

# Or install all dependencies (including dev)
pip install -r requirements/base.txt
pip install -r requirements/local.txt

# Run the downloader
python main_noplaylist.py  # Download a single video
python main_playlist.py    # Download a playlist
python main_loop_noplaylist.py  # Loop mode (single video)
python main_loop_playlist.py    # Loop mode (playlist)
```

## Development Workflow

```bash
# Download a single video
python main_noplaylist.py

# Download a playlist
python main_playlist.py

# Run in loop mode for batch processing
python main_loop_playlist.py

# Run tests
python test.py
```

## Testing Instructions

```bash
# Run the test suite
python test.py

# Type checking (if mypy configured)
mypy *.py

# Lint checking (if ruff configured)
ruff check .
```

## Code Style

- **Python**: PEP 8, type hints encouraged
- **Naming**: snake_case for functions and files
- **Scripts**: Each main script has a clear purpose (noplaylist vs playlist, single vs loop)
- **Error handling**: Try/except blocks for network and download failures
- **CLI**: Simple command-line interface

## Build/Deployment

```bash
# No build step — run directly
python main_noplaylist.py
```

This is a CLI tool, not a web service. No deployment configuration needed.

## Security

- Validate URLs before downloading — avoid SSRF via malicious URLs
- Downloaded content should be scanned for malware
- Respect YouTube's Terms of Service and copyright
- Do not use for mass downloading or commercial purposes
- Keep yt-dlp updated to handle site changes

## Troubleshooting

- **yt-dlp errors**: Update yt-dlp with `pip install -U yt-dlp`
- **Download fails**: Verify the video URL is accessible and not age-restricted
- **Playlist issues**: Check playlist visibility settings (private vs public)
- **curl_cffi errors**: Ensure curl_cffi is properly installed for your platform
- **FFmpeg not found**: Some format conversions require FFmpeg — install separately
- **Rate limiting**: YouTube may throttle excessive downloads — add delays between requests
