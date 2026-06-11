# YouTube Downloader

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A Python-based YouTube video downloader with playlist support and continuous loop mode.

## Features

- ✅ Download individual YouTube videos with quality selection
- ✅ Download entire YouTube playlists
- ✅ Loop mode for continuous batch downloading
- ✅ Multiple quality options (720p, 1080p, etc.)
- ✅ Simple command-line interface
- ✅ Built-in test suite

## Requirements

- Python 3.x
- yt-dlp with curl_cffi support
- Additional development dependencies listed in requirements/

## Installation

1. Clone or download this repository:
```bash
cd youtube-downloader
```

2. Install dependencies:
```bash
pip install -r requirements/local.txt
```

Or for production (minimal dependencies):
```bash
pip install -r requirements/base.txt
```

## Available Scripts

| Script | Description | Use Case |
| --- | --- | --- |
| `main_noplaylist.py` | Download a single YouTube video | One-time video download |
| `main_playlist.py` | Download an entire YouTube playlist | Download all videos from a playlist |
| `main_loop_noplaylist.py` | Continuously download videos in a loop | Batch download multiple videos |
| `main_loop_playlist.py` | Continuously download playlists in a loop | Batch download multiple playlists |
| `test.py` | Test suite | Verify functionality |

## Usage

### Download a Single Video

```bash
python main_noplaylist.py
```

When prompted:
1. Enter a YouTube video URL
2. Select your preferred quality option (e.g., 1 for 720p, 2 for 1080p)
3. Wait for download to complete

**Example:**
```
Enter YouTube URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Select quality (1-720p, 2-1080p): 2
Downloading... Done!
```

### Download a Playlist

```bash
python main_playlist.py
```

When prompted:
1. Enter a YouTube playlist URL
2. Videos will download sequentially

**Example:**
```
Enter Playlist URL: https://www.youtube.com/playlist?list=PLxxxxx
Downloading playlist... (Video 1/25) [████████] 100%
```

### Continuous Video Download (Loop Mode)

```bash
python main_loop_noplaylist.py
```

Keeps running and prompts for new video URLs after each download completes. Perfect for:
- Batch downloading videos throughout the day
- Processing multiple URLs without restarting

### Continuous Playlist Download (Loop Mode)

```bash
python main_loop_playlist.py
```

Keeps running and prompts for new playlist URLs after each download completes. Useful for:
- Downloading content from multiple channels sequentially
- Archiving playlists over time

### Run Tests

```bash
python test.py
```

Verifies that:
- yt-dlp is properly installed
- Download functionality is working
- Quality selection works correctly

## Troubleshooting

### "yt-dlp not found" error
Install yt-dlp with curl support:
```bash
pip install yt-dlp[curl-cffi]
```

### "Invalid URL" error
Make sure you're using valid YouTube URLs:
- Single video: `https://www.youtube.com/watch?v=VIDEO_ID`
- Playlist: `https://www.youtube.com/playlist?list=PLAYLIST_ID`

### Download fails
- Check your internet connection
- Ensure yt-dlp is up to date: `pip install --upgrade yt-dlp`
- Try a different video (YouTube restrictions may apply)

## Directory Structure

```
youtube-downloader/
├── main_noplaylist.py       # Single video downloader
├── main_playlist.py         # Playlist downloader
├── main_loop_noplaylist.py  # Single video loop mode
├── main_loop_playlist.py    # Playlist loop mode
├── test.py                  # Test suite
├── requirements/
│   ├── base.txt            # Production dependencies
│   └── local.txt           # Dev & production dependencies
├── README.md               # This file
└── LICENSE                 # MIT License
```

## Development

For development work, install with dev dependencies:
```bash
pip install -r requirements/local.txt
```

Dev tools included:
- pytest - Testing framework
- mypy - Type checking
- ruff - Code linting
- black - Code formatting
- coverage - Test coverage analysis

## License

This project is licensed under the MIT License - see [LICENSE](./LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
