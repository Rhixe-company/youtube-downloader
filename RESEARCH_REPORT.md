# RESEARCH_REPORT.md

## Project: youtube-downloader

**Type:** YouTube CLI download tool
**Tech Stack:** Python 3.x, yt-dlp[curl-cffi], FFmpeg, ruff, mypy, uv, pytest
**Status:** Active

---

## Similar Projects

| Project | URL | Why Relevant |
|---------|-----|--------------|
| Python-projects | `projects/Python-projects` | shared Python CLI + requirements hygiene |
| selenium_webdriver | `projects/selenium_webdriver` | browser automation alternative for scraping |

---

## Key Findings

### yt-dlp + curl_cffi Best Practices (2026)

- **yt-dlp is gold standard** — 100K+ stars, 1,800+ sites, daily updates
- **Install `yt-dlp[curl-cffi]`** — `--impersonate chrome` bypasses bot protection
- **`--download-archive archive.txt`** — skip already-downloaded content; essential for cron jobs
- **`-o` output template** — `%(channel)s/%(upload_date)s_%(id)s.%(ext)s`; always include `%(id)s` to avoid title collisions
- **Cookie support** — `--cookies-from-browser firefox` for gated content; `--cookies cookies.txt` for headless
- **Format selector syntax** — default `bv*+ba/b` (best video + best audio / best combined); use `bv*[height<=1080]+ba*[ext=m4a]` for capped quality
- **Extractor args for YouTube** — `--extractor-args "youtube:player_client=web,web_safari"` when player changes break extraction
- **Post-processing** — `--embed-metadata --embed-thumbnail --embed-subs --embed-chapters` embeds everything in one pass
- **Merge output** — `--merge-output-format mp4` forces MP4 container after merging

### curl_cffi for YouTube Bot Protection Bypass (2026)

- **curl_cffi is a Python binding for curl-impersonate** — mimics real browser TLS/JA3/HTTP2 fingerprints
- **Install via `pip install "yt-dlp[curl-cffi]"`** or `pip install curl_cffi` directly
- **Usage with yt-dlp** — yt-dlp automatically uses curl_cffi when available for `--impersonate chrome`
- **Key impersonation targets** — `chrome`, `safari`, `safari_ios`, `firefox`, `edge`
- **Limitations** — beats TLS/HTTP2 fingerprinting; does NOT solve JavaScript challenges (Cloudflare Turnstile, etc.)
- **Works at network layer** — request looks like real browser before any HTTP headers sent

### YouTube Scraping & Legal Landscape (2026)

- **2026 DMCA ruling** — third-party downloading ruled as copyright circumvention; personal use only
- **YouTube ToS vs Copyright Law** — ToS violation is civil/contract; DMCA 1201 anti-circumvention is criminal
- **RIAA vs youtube-dl (2020)** — tool itself not infringing; distribution for infringing use is the risk
- **Personal use defense** — format-shifting for personal archive generally considered fair use in US
- **Creative Commons content** — explicitly downloadable; filter with `--match-filter "license!=*"` 
- **YouTube Premium** — official offline download; only legal method for copyrighted content
- **Rate limiting as compliance** — `--limit-rate 5M --sleep-interval 5 --max-sleep-interval 15` demonstrates good faith

### Python CLI Design (2026)

- **PEP 723** inline script metadata — `# /// script` block embeds dependencies for standalone scripts
- **Typer** — type-hint-driven; best for multi-command tools in 2026
- **Click** — mature decorator-based; shell autocomplete via `click-completion`
- **argparse** — stdlib; zero-dep for simple single-command tools
- **Rich** — pretty console output, progress bars, tables; pairs well with any CLI framework

### Python Tooling 2026

- **uv** — replaces pip + venv + poetry; 10-100x faster, Rust-based, lock files
- **Ruff** — replaces black + flake8 + isort; 800+ rules, runs in ms
- **mypy strict mode** — production baseline; `--strict` catches real bugs
- **ty (Astral)** — new Rust-based type checker from Ruff/uv creators; 10-50x faster than mypy; beta 2026; finds bugs without type annotations
- **pytest** — standard; `pytest-sugar` for nicer output; `pytest-cov` for coverage

### FFmpeg Post-Processing

- **FFmpeg required** for stream merging, audio extraction, thumbnails
- **yt-dlp does NOT bundle ffmpeg** — must install separately
- **`--merge-output-format mp4`** triggers automatic ffmpeg merging
- **Audio extraction** — `-x --audio-format mp3 --audio-quality 0`
- **Video conversion** — `--recode-video mp4` or `--postprocessor-args`
- **Embed metadata** — `--embed-metadata` writes title, description, upload_date, etc. as ID3/MP4 tags
- **Embed thumbnail** — `--embed-thumbnail` + `--convert-thumbnails jpg` for compatibility
- **Embed subtitles** — `--embed-subs --sub-langs en` burns or embeds subs
- **Concurrent fragments** — `-N 4` speeds up HLS/DASH but throttle to avoid blocks

### YouTube Rate Limiting & Polite Scraping (2026)

- **Rate limit options** — `--limit-rate 5M` (5 MB/s), `--sleep-interval 5`, `--max-sleep-interval 15`
- **Retry logic** -- `--retries 20 --fragment-retries 20 --retry-sleep linear=1::2`
- **Download archive** — `--download-archive archive.txt` skips completed; essential for resumable runs
- **Concurrent fragments** — `-N 4` for speed; reduce if getting 429 errors
- **Player client rotation** — `--extractor-args "youtube:player_client=web,web_safari,android,android_vr"` for format availability
- **Cookie rotation** — use `--cookies-from-browser` with profile rotation for authenticated access
- **Proxy support** — `--proxy http://user:pass@host:port` for IP rotation
- **IPv6 vs IPv4** — YouTube sometimes throttles IPv6; force IPv4 with `--force-ipv4`

### Format Selection Deep Dive (2026)

- **Default** — `bv*+ba/b` (best video + best audio / best combined)
- **Cap at 1080p** — `bv*[height<=1080]+ba*[ext=m4a]` (avoids 4K throttling)
- **MP4 only** — `bv*[ext=mp4]+ba*[ext=m4a]` (widest compatibility)
- **Specific codecs** — `bv*[vcodec^=avc1]+ba*[acodec^=mp4a]` (H.264/AAC only)
- **List formats** — `-F` shows all available format codes
- **Format sorting** — `-S res,ext:mp4:m4a,br,size` custom priority
- **Audio only** — `-x --audio-format mp3 --audio-quality 0`
- **Merge to MP4** — `--merge-output-format mp4` forces container after merge

### YouTube API vs yt-dlp for Metadata

| Aspect | YouTube Data API v3 | yt-dlp |
|--------|---------------------|--------|
| Quota | 10,000 units/day | Unlimited |
| Auth | API key / OAuth | Cookies optional |
| Metadata depth | Structured, limited fields | Full raw extraction |
| Geo-blocked content | Requires region param | Works with cookies |
| Rate limits | Strict quotas | Self-imposed delays |
| Maintenance | Google maintained | Community daily updates |
| Live streams | Limited support | Full support |
| Comments | Separate endpoint | Included in extraction |
| Channel videos | Paginated playlist | `--flat-playlist` dump |
| Legal risk | Official, ToS-compliant | Gray area (ToS violation) |

**Recommendation** — Use YouTube API for structured, quota-bound apps; yt-dlp for bulk extraction, archival, and unrestricted access.

### Python Packaging for yt-dlp CLI Tools (2026)

- **Dependency spec** — `yt-dlp[curl-cffi]` in `pyproject.toml` or `requirements.txt`
- **Optional deps** — `[curl-cffi]` extras pulls curl_cffi + dependencies
- **Lock file** — `uv lock` generates `uv.lock` for reproducible installs
- **Entry points** — `[project.scripts]` in `pyproject.toml` for `pipx install` or `uv tool install`
- **Standalone scripts** — PEP 723 `# /// script` block for zero-install execution
- **Binary distribution** — PyInstaller or `uv build` for standalone executables
- **Version pinning** — `yt-dlp>=2026.1.0,<2027` for stability

---

## Cheatsheets & Quick Reference

| Topic | Resource | Type |
|-------|----------|------|
| yt-dlp 2026 | <https://dev.to/pickuma/yt-dlp-the-cli-video-downloader-developers-actually-use-in-2026-57jk> | Guide |
| yt-dlp repo | <https://github.com/yt-dlp/yt-dlp#readme> | CLI docs |
| curl_cffi | <https://github.com/yifeikong/curl_cffi> | TLS fingerprint library |
| Python tooling | <https://softaims.com/blog/modern-python-tooling-uv-ruff-mypy-2026> | Guide |
| FFmpeg Python | <https://github.com/kkroening/ffmpeg-python> | Python FFmpeg wrapper |
| yt-dlp post-processing | <https://yt-dlp-yt-dlp.mintlify.app/guides/post-processing> | Official guide |
| yt-dlp download options | <https://yt-dlp-yt-dlp.mintlify.app/cli/download-options> | Official CLI ref |
| yt-dlp format selection | <https://yt-dlp-yt-dlp.mintlify.app/cli/format-selection> | Official guide |
| Format selector examples | <https://www.ditig.com/yt-dlp-cheat-sheet> | Cheatsheet |
| yt-dlp extractor args | <https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/extractor/youtube.py> | Source reference |

---

## Best Practices

1. **`pipx install yt-dlp[curl-cffi]`** — isolated env; `--impersonate chrome` for bot protection
2. **`--download-archive archive.txt`** — skip completed downloads; essential for automation
3. **Output template with `%(id)s`** — prevents filename collisions from title changes
4. **`--cookies-from-browser`** — access gated/age-restricted content without manual login
5. **Rate limiting** — `--limit-rate 5M --sleep-interval 5` for unattended jobs
6. **Format selection** — `bv*[height<=1080]+ba*[ext=m4a]` balances quality/speed
7. **Merge to MP4** — `--merge-output-format mp4` for universal playback
8. **Embed everything** — `--embed-metadata --embed-thumbnail --embed-subs --embed-chapters`
9. **Update yt-dlp weekly** — `pip install -U yt-dlp` or `yt-dlp -U` for site fixes
10. **Validate URLs** — regex allowlist `(youtube\.com|youtu\.be)` only; reject `file://`, localhost, internal IPs

---

## Common Pitfalls

| Pitfall | Impact | Avoidance |
|---------|--------|-----------|
| Unbounded filenames | FS conflicts | sanitize; include `%(id)s` in template |
| Missing curl_cffi | `--impersonate` fails | `pip install "yt-dlp[curl-cffi]"` |
| No FFmpeg in PATH | silent post-proc failure | detect at startup; fail fast |
| Aggressive rate limiting | IP blocks, CAPTCHAs | 5-6s delays; proxies |
| Player client extraction failure | 404/error pages | `--extractor-args "youtube:player_client=web,web_safari"` |
| Missing `%(id)s` in output | overwrites on title change | always include unique ID |
| No download archive | re-downloads on rerun | `--download-archive archive.txt` |
| Hardcoded format codes | breaks when YouTube changes | use selector syntax `bv*+ba` |

---

## Performance

1. **Reuse `YoutubeDL` instance** — avoids re-init per playlist item
2. **`--no-overwrites` + `--write-info-json`** — skip completed, cache metadata
3. **Limit quality** — `bestvideo[height<=1080]+bestaudio` avoids unnecessary 4K
4. **`--concurrent-fragments`** — speed up but throttle to avoid blocks
5. **Flat playlist extraction** — `--flat-playlist` for URL-only enumeration
6. **Skip DASH manifest** — `--skip-download --get-url` for direct stream URLs

---

## Security

1. **Validate YouTube URLs** — regex allowlist: `(youtube\.com|youtu\.be)` only
2. **No arbitrary domains** — reject `file://`, localhost, internal IPs
3. **DMCA awareness** — 2026 ruling: third-party downloading as circumvention; personal use only
4. **Cookie files** — treat as secrets; never commit `cookies.txt`
5. **SSRF prevention** — validate URL scheme/host before passing to yt-dlp
6. **Subprocess injection** — never shell-interpolate URLs; pass as list args

---

## Related Projects (in workspace)

- **Python-projects** — shared Python CLI pattern and dependency hygiene
- **selenium_webdriver** — browser automation for JS-heavy sites

---

## Resources

| Resource | URL | Description |
|----------|-----|-------------|
| yt-dlp docs | <https://github.com/yt-dlp/yt-dlp#readme> | CLI documentation |
| curl_cffi | <https://github.com/yifeikong/curl_cffi> | TLS fingerprint library |
| FFmpeg Python | <https://github.com/kkroening/ffmpeg-python> | Python FFmpeg wrapper |
| YouTube scraping | <https://dev.to/pickuma/yt-dlp-the-cli-video-downloader-developers-actually-use-in-2026-57jk> | Method decision matrix |
| yt-dlp post-processing | <https://yt-dlp-yt-dlp.mintlify.app/guides/post-processing> | Official post-proc guide |
| yt-dlp format selection | <https://yt-dlp-yt-dlp.mintlify.app/cli/format-selection> | Format selector reference |
| yt-dlp cheat sheet | <https://www.ditig.com/yt-dlp-cheat-sheet> | Quick reference |
| yt-dlp extractor args | <https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/extractor/youtube.py> | YouTube extractor source |
| YouTube Data API | <https://developers.google.com/youtube/v3/docs> | Official API reference |

---

## Project Codebase Analysis (Current State)

### Scripts Overview

| Script | Purpose | Key Configuration |
|--------|---------|-------------------|
| `main_noplaylist.py` | Single video download | `noplaylist=True`, format `136+ba,298+ba,232+ba,bv+ba`, MKV merge |
| `main_playlist.py` | Playlist download | `noplaylist=False`, playlist-aware output template |
| `main_loop_playlist.py` | Batch loop mode | Iterates URL list, same opts as playlist |
| `main_loop_noplaylist.py` | Batch single videos | Iterates URL list, single-video opts |
| `test.py` | Basic test | Interactive URL input, MP4 convert, EN/FR subs |

### Current Configuration Patterns

**Format Selection** — Uses hardcoded format codes (`136`, `298`, `232`) + fallback `bv+ba`
- **Issue**: Format codes change; selector syntax `bv*+ba` is more robust
- **Recommendation**: Migrate to `bv*[height<=1080]+ba*[ext=m4a]`

**Post-Processing** — Uses `FFmpegVideoConvertor` to MKV/MP4
- **Missing**: `--embed-metadata`, `--embed-thumbnail`, `--embed-subs`, `--embed-chapters`
- **Recommendation**: Add full embed chain for archival quality

**Rate Limiting** — Not configured in scripts
- **Missing**: `--limit-rate`, `--sleep-interval`, `--download-archive`
- **Recommendation**: Add polite defaults; make configurable via CLI args

**Cookies/Auth** — Not configured
- **Missing**: `--cookies-from-browser` support
- **Recommendation**: Add optional cookie browser arg for gated content

**Output Templates** — Uses `%(uploader)s/%(title)s.%(ext)s` or playlist-aware variant
- **Missing**: `%(id)s` for collision avoidance; `%(upload_date)s` for sorting
- **Recommendation**: Standardize on `%(channel)s/%(upload_date)s_%(id)s.%(ext)s`

### Dependencies

**`requirements/local.txt`** (dev environment):
```
-r ./base.txt
mypy
pytest
pytest-sugar
sphinx
sphinx-autobuild
ruff
coverage
djlint
pre-commit
factory-boy
black
#yt-dlp
yt-dlp[curl-cffi]
```

**Observations:**
- `yt-dlp[curl-cffi]` correctly specified with extras
- `base.txt` contains many unrelated dev deps (sphinx, jinja2, etc.) — should be split
- Missing: `uv`, `ty` (new type checker), `rich` (for CLI output)
- Consider `pyproject.toml` with `[project]` and `[tool.ruff]` config

---

## Recommended Improvements

### 1. Unified CLI Entry Point
Replace 4 scripts with single Typer app:
```python
# cli.py
import typer
from yt_dlp import YoutubeDL

app = typer.Typer()

@app.command()
def video(url: str, quality: str = "1080p", ...):
    ...

@app.command()
def playlist(url: str, ...):
    ...

@app.command()
def batch(file: typer.FileText, ...):
    ...
```

### 2. Configuration Management
- `config.yaml` or `pyproject.toml` for defaults
- Environment variable overrides
- CLI flags take precedence

### 3. Robust Defaults
```python
DEFAULT_OPTS = {
    "format": "bv*[height<=1080]+ba*[ext=m4a]/bv*+ba/b",
    "merge_output_format": "mp4",
    "writeautomaticsub": True,
    "subtitlesformat": "srt",
    "subtitleslangs": ["en"],
    "writethumbnail": True,
    "embed_thumbnail": True,
    "embed_metadata": True,
    "embed_subs": True,
    "embed_chapters": True,
    "download_archive": "archive.txt",
    "limit_rate": "5M",
    "sleep_interval": 5,
    "max_sleep_interval": 15,
    "retries": 20,
    "fragment_retries": 20,
    "concurrent_fragment_downloads": 4,
    "extractor_args": {"youtube": {"player_client": ["web", "web_safari"]}},
}
```

### 4. URL Validation & Security
```python
YOUTUBE_URL_PATTERN = re.compile(
    r"^https?://(www\.)?(youtube\.com|youtu\.be)/.+$"
)

def validate_url(url: str) -> bool:
    return bool(YOUTUBE_URL_PATTERN.match(url))
```

### 5. Progress & Logging
- Use `rich.progress` for beautiful console output
- Structured logging with `loguru` or stdlib `logging`
- JSON log output option for CI/automation

### 6. Testing
- Unit tests for URL validation, config merging
- Integration tests with `--flat-playlist` (no download)
- Mock yt-dlp for fast CI runs

---

*Report generated by web-research-pipeline — last updated 2026-07-10*