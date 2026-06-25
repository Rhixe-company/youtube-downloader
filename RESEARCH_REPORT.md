# RESEARCH_REPORT.md

<!-- Template version: 1.0.0 — size gate: 1KB-5KB -->

## Project: youtube-downloader
**Type:** YouTube CLI download tool
**Tech Stack:** Python 3.x, yt-dlp, curl_cffi, pytest, mypy, ruff, black
**Status:** Active

---

## Similar Projects

| Project | URL | Why Relevant |
|---------|-----|--------------|
| Python-projects | `projects/Python-projects` | Shared Python CLI + requirements hygiene pattern. |
| selenium_webdriver | `projects/selenium_webdriver` | Browser automation alternatives for scraping. |

---

## Key Findings

### yt-dlp + curl_cffi Best Practices (2026)
- **yt-dlp is gold standard** — daily updates, 1800+ sites [DevKantKumar 2026]
- **Install `yt-dlp[curl-cffi]`** — enables `--impersonate chrome` for bot protection [Stack Overflow]
- **Rate limiting**: YouTube enforces 5-6s sleeps; 75% block rate for aggressive use [r/youtubedl]
- **Version pinning**: pin in requirements; `--no-update` for reproducibility [DevKantKumar 2026]

### YouTube Scraping & Legal Landscape (2026)
- **2026 DMCA ruling**: third-party downloads ruled as copyright circumvention [Medianama Feb 2026]
- **Method matrix**: yt-dlp for deep pulls; Data API v3 for low-volume (10K units/day) [WebScrapingAPI 2026]
- **Ethical scraping**: polite delays, respect robots.txt, proxies [WebScrapingAPI 2026]

### Python CLI Design (2026)
- **argparse** — zero deps, best for single-file scripts [Stackify 2026]
- **Typer** — type-hint-driven, auto-help; for multi-command tools [Typer docs]
- **Click** — mature decorator-based; shell autocomplete [r/learnpython]

### Testing & CI Pipeline (2026)
- **Ruff** replaces black+flake8+isort — 10-100x faster [Softaims 2026]
- **mypy strict mode** — production baseline for type safety [Softaims 2026]
- **uv** replaces pip+venv+tools — 10-100x faster with lock files [Softaims 2026]
- **CI**: `ruff check .` → `ruff format . --check` → `mypy .` → `pytest` [Softaims 2026]

### FFmpeg Post-Processing (2026)
- **`ffmpeg-python`** — Pythonic wrapper (import `ffmpeg`) [Templated.io]
- **Common**: MP4↔WebM, audio extraction, trimming, thumbnails [Templated.io]
- **Caveat**: FFmpeg binary must be installed separately [Templated.io]

---

## Cheatsheets & Quick Reference

| Topic | Resource | Type |
|-------|----------|------|
| yt-dlp 2026 | https://www.devkantkumar.com/blog/yt-dlp-ultimate-guide-2026 | Guide |
| yt-dlp repo | https://github.com/yt-dlp/yt-dlp#readme | CLI docs |
| YouTube scraping | https://www.webscrapingapi.com/how-to-scrape-youtube | Guide |
| Python tooling | https://softaims.com/blog/modern-python-tooling-uv-ruff-mypy-2026 | Guide |
| FFmpeg Python | https://templated.io/blog/ffmpeg-in-python-a-practical-guide-with-code-examples | Guide |

---

## Best Practices

1. **Explicit CLI** — `download --url URL --quality 1080p` enables automation
2. **Pin yt-dlp** — version in requirements; `--no-update` for reproducibility
3. **Install `yt-dlp[curl-cffi]`** — `--impersonate chrome` bypasses bot protection
4. **Adopt uv + Ruff + mypy** — modern Python toolchain in pyproject.toml
5. **Use ffmpeg-python** — cleaner post-processing than subprocess

---

## Common Pitfalls

| Pitfall | Impact | Avoidance |
|---------|--------|-----------|
| Unbounded filenames | FS conflicts | Sanitize + prefix |
| Missing curl_cffi | `--impersonate` fails | Install `yt-dlp[curl-cffi]` |
| No FFmpeg in PATH | Silent post-proc failure | Detect at startup |
| Aggressive rate limit | IP blocks, CAPTCHAs | 5-6s delays; proxies |

---
---
## Performance
1. **Reuse `YoutubeDL` instance** — avoids re-init per playlist item
2. **`--no-overwrites` + `--write-info-json`** — skip completed, cache metadata
3. **Limit quality** — `bestvideo[height<=1080]+bestaudio` avoids unnecessary 4K

---
## Security
1. **Validate YouTube URLs** — regex allowlist: `(youtube\.com|youtu\.be)` only
2. **No arbitrary domains** — reject `file://`, `localhost`, internal IPs
3. **DMCA awareness** — 2026 ruling: third-party downloading as circumvention; personal use only

---
## Related Projects (in workspace)
- **Python-projects** — shared Python CLI and dependency hygiene
- **selenium_webdriver** — browser automation for JS-heavy sites

---

## Resources

| Resource | URL | Description |
|----------|-----|-------------|
| yt-dlp docs | https://github.com/yt-dlp/yt-dlp#readme | CLI documentation |
| curl_cffi | https://github.com/yifeikong/curl_cffi | TLS fingerprint library |
| FFmpeg Python | https://github.com/kkroening/ffmpeg-python | Python FFmpeg wrapper |
| YouTube scraping | https://www.webscrapingapi.com/how-to-scrape-youtube | Method decision matrix |
| Python tooling | https://softaims.com/blog/modern-python-tooling-uv-ruff-mypy-2026 | uv + Ruff + mypy guide |
