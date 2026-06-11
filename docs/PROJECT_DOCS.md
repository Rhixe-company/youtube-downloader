# YouTube Downloader — Project Documentation

## Overview

A collection of Python CLI scripts for downloading YouTube videos and playlists using yt-dlp. Supports single video downloads, full playlist downloads, and batch processing from URL files. Videos are saved as MKV with embedded subtitles, metadata, and thumbnails.

**Repository:** https://github.com/Rhixe-company/youtube-downloader  
**Stack:** Python 3.8+ | yt-dlp | ffmpeg  
**Status:** Stable / Maintenance

---

## Quick Start

### Prerequisites

```bash
# Python 3.8+
python --version

# Install yt-dlp
pip install yt-dlp

# Install ffmpeg (system dependency)
#   Windows: choco install ffmpeg
#   macOS:   brew install ffmpeg
#   Linux:   sudo apt install ffmpeg
```

### Download a Single Video

```bash
python main_noplaylist.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Download a Playlist

```bash
python main_playlist.py "https://www.youtube.com/playlist?list=PL..."
```

### Download from a URL File

```bash
# Create urls.txt with one URL per line
python main_loop_noplaylist.py urls.txt
python main_loop_playlist.py playlist_urls.txt
```

---

## Architecture

### Script Architecture

The project uses a flat, single-file design — each script is standalone and self-contained:

```
youtube-downloader/
├── main_noplaylist.py      # Single video download
├── main_playlist.py        # Playlist download
├── main_loop_noplaylist.py # Batch single video downloads from file
├── main_loop_playlist.py   # Batch playlist downloads from file
├── docs/
│   ├── CODE_DOCS.md        # Code reference
│   ├── PROJECT_DOCS.md     # This file
│   └── audit-report.md     # Security audit
└── downloads/              # Default output directory
```

### Data Flow

```
YouTube URL
    │
    ▼
┌──────────────┐
│  main_*.py    │
│  argparse     │
│  (CLI Input)  │
└──────┬───────┘
       │ URL
       ▼
┌──────────────┐
│  yt-dlp       │
│  YoutubeDL    │
│  extract_info │
└──────┬───────┘
       │ Streams
       ▼
┌──────────────┐
│  ffmpeg       │
│  (merge)      │
│  (mux)        │
└──────┬───────┘
       │ MKV
       ▼
┌──────────────┐
│  Output File  │
│  Title.mkv    │
│  (with subs + │
│   thumbnail)  │
└──────────────┘
```

### Key Design Decisions

1. **Flat script structure** — No shared modules or packages; each script is independently usable
2. **MKV container** — Chosen for broad codec support and metadata embedding capabilities
3. **720p target** — Format `136+ba` targets 720p H.264 for good quality/bandwidth balance
4. **Sequential processing** — No parallel downloads; reduces risk of IP throttling
5. **Minimal dependencies** — Only yt-dlp + ffmpeg; no web frameworks or databases

---

## Developer Guide

### Project Setup

```bash
# Clone repository
git clone https://github.com/Rhixe-company/youtube-downloader.git
cd youtube-downloader

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install yt-dlp
pip install yt-dlp
```

### Verifying ffmpeg Installation

```bash
# Check ffmpeg is available
ffmpeg -version

# yt-dlp will report missing ffmpeg
yt-dlp --version
```

### Testing Downloads

```bash
# Test single download (short video)
python main_noplaylist.py "https://www.youtube.com/watch?v=jNQXAC9IVRw" --output test_output

# Test playlist (limit to 2 videos)
python main_playlist.py "https://www.youtube.com/playlist?list=PL..." --limit 2 --output test_output
```

### Customization Guide

To modify video quality, edit the `format` option in each script:

```python
# For 1080p max:
'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'

# For 4K max:
'format': 'bestvideo[height<=2160]+bestaudio/best[height<=2160]'

# For lowest size:
'format': 'worstvideo+worstaudio/worst'

# Audio only:
'format': 'bestaudio/best',
'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
```

### Adding New Features

To extend the scripts:

1. Copy an existing script as a template
2. Modify `ydl_opts` dictionary for new yt-dlp options
3. Update CLI arguments if needed
4. Test with various YouTube URLs (public, unlisted, age-restricted)

---

## User Guide

### Single Video Download

```bash
# Basic usage
python main_noplaylist.py <URL>

# Custom output directory
python main_noplaylist.py <URL> --output ./my_videos

# Example
python main_noplaylist.py "https://youtu.be/dQw4w9WgXcQ"
```

### Playlist Download

```bash
# Download entire playlist
python main_playlist.py <PLAYLIST_URL>

# Limit number of videos
python main_playlist.py <PLAYLIST_URL> --limit 10

# Custom directory
python main_playlist.py <PLAYLIST_URL> --output ./my_playlists

# Example
python main_playlist.py "https://youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf"
```

### Batch Download from File

Create a text file with URLs (one per line):

```
# urls.txt
https://www.youtube.com/watch?v=video1
https://www.youtube.com/watch?v=video2
https://www.youtube.com/playlist?list=PL...
```

Then run:

```bash
python main_loop_noplaylist.py urls.txt
python main_loop_playlist.py playlist_urls.txt
```

### Output Structure

```
downloads/
├── My Video Title.mkv              # From main_noplaylist.py
└── My Playlist Name/               # From main_playlist.py
    ├── 1 - First Video.mkv
    ├── 2 - Second Video.mkv
    └── 3 - Third Video.mkv
```

### What You Get

Each `.mkv` file includes:
- **Video stream** — 720p H.264 (or best available)
- **Audio stream** — Best available (AAC/Opus)
- **Subtitles** — English (manual + auto-generated)
- **Thumbnail** — Embedded as cover art
- **Metadata** — Title, uploader, description, upload date

---

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| `yt-dlp: command not found` | yt-dlp not installed | `pip install yt-dlp` |
| `ffmpeg not found` | ffmpeg not installed | Install ffmpeg via system package manager |
| `HTTP Error 429` | Rate limited by YouTube | Add `'sleep_interval': 5` to ydl_opts |
| `[Private video]` | Video is private | Cannot download private videos |
| `[Age-restricted]` | Age-restricted content | Add `'age_limit': 18` or use YouTube cookies |
| `No video formats found` | Region/copyright block | Use VPN or proxy |
| File not merging | ffmpeg version issue | Update ffmpeg to latest version |

### Adding Cookie Support for Restricted Content

To download age-restricted or member-only content:

```python
ydl_opts = {
    # ... other options ...
    'cookiefile': 'cookies.txt',  # Export from browser extension
}
```

Export cookies using a browser extension (e.g., "Get cookies.txt" for Chrome/Firefox).

---

## Contributing

### Quick Guidelines

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/description`
3. Make changes following the existing script pattern
4. Test with a variety of YouTube URLs
5. Update documentation for significant changes
6. Submit a pull request

### Code Style

- Follow PEP 8 conventions
- Use descriptive variable names
- Add Google-style docstrings for all functions
- Keep scripts independent (no cross-script imports)
- Keep each script under 200 lines

### Testing

Currently there are no automated tests. Manual testing:

```bash
# Test with public video
python main_noplaylist.py "https://www.youtube.com/watch?v=jNQXAC9IVRw"

# Test with playlist
python main_playlist.py "https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf" --limit 2

# Verify output
ls downloads/
ffprobe downloads/*.mkv  # Check file integrity
```

---

## Known Limitations

- No resume support for interrupted downloads
- No download queue or parallel downloading
- No GUI — CLI only
- No automatic retry on network errors
- No update checking for yt-dlp
- Hardcoded output path defaults to `./downloads/`
- Limited format selection for some age-restricted videos
