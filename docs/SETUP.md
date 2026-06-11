# Setup Guide

## Prerequisites

- Python 3.8+
- pip
- Git

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd youtube-downloader
```

2. Create virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows
```

3. Install dependencies:
```bash
pip install -r requirements/local.txt
```

## Usage

Each script is run independently:
```bash
python main_noplaylist.py      # Single video
python main_playlist.py        # Playlist
python main_loop_noplaylist.py # Loop mode
python main_loop_playlist.py   # Playlist loop
```

## Common Commands

| Command | Description |
| --- | --- |
| `python test.py` | Run test suite |
| `python -m pytest` | Run pytest |
| `ruff check .` | Run linter |

## Troubleshooting

If you encounter issues:
1. Verify Python version (3.8+)
2. Update yt-dlp: `pip install --upgrade yt-dlp`
3. Check your internet connection