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

### YouTube Scraping & Legal Landscape (2026)
- 2026 DMCA ruling: third-party downloads as copyright circumvention — personal use only
- `--extractor-args "youtube:player_client=web,web_safari"` when YouTube player changes break extraction
- Rate limiting: `--limit-rate 5M --sleep-interval 5 --max-sleep-interval 15` to avoid 429 blocks

### Python CLI Design (2026)
- **PEP 723** inline script metadata — `# /// script` block embeds dependencies for standalone scripts
- **Typer** — type-hint-driven; best for multi-command tools in 2026
- **Click** — mature decorator-based; shell autocomplete via `click-completion`

### Python Tooling 2026
- **uv** — replaces pip + venv + poetry; 10-100x faster, Rust-based, lock files
- **Ruff** — replaces black + flake8 + isort; 800+ rules, runs in ms
- **mypy strict mode** — production baseline

### FFmpeg Post-Processing
- FFmpeg required for stream merging, audio extraction, thumbnails
- yt-dlp does NOT bundle ffmpeg — must install separately
- `--merge-output-format mp4` triggers automatic ffmpeg merging

---

## Cheatsheets & Quick Reference

| Topic | Resource | Type |
|-------|----------|------|
| yt-dlp 2026 | https://dev.to/pickuma/yt-dlp-the-cli-video-downloader-developers-actually-use-in-2026-57jk | Guide |
| yt-dlp repo | https://github.com/yt-dlp/yt-dlp#readme | CLI docs |
| curl_cffi | https://github.com/yifeikong/curl_cffi | TLS fingerprint library |
| Python tooling | https://softaims.com/blog/modern-python-tooling-uv-ruff-mypy-2026 | Guide |
| FFmpeg Python | https://github.com/kkroening/ffmpeg-python | Python FFmpeg wrapper |

---

## Best Practices

1. **`pipx install yt-dlp[curl-cffi]`** — isolated env; `--impersonate chrome` for bot protection
2. **`--download-archive archive.txt`** — skip completed downloads; essential for automation
3. **Output template with `%(id)s`** — prevents filename collisions from title changes
4. **`--cookies-from-browser`** — access gated/age-restricted content without manual login
5. **Rate limiting** — `--limit-rate 5M --sleep-interval 5` for unattended jobs

---

## Common Pitfalls

| Pitfall | Impact | Avoidance |
|---------|--------|-----------|
| Unbounded filenames | FS conflicts | sanitize; include `%(id)s` in template |
| Missing curl_cffi | `--impersonate` fails | `pip install "yt-dlp[curl-cffi]"` |
| No FFmpeg in PATH | silent post-proc failure | detect at startup; fail fast |
| Aggressive rate limiting | IP blocks, CAPTCHAs | 5-6s delays; proxies |
| Player client extraction failure | 404/error pages | `--extractor-args "youtube:player_client=web,web_safari"` |

---

## Performance

1. **Reuse `YoutubeDL` instance** — avoids re-init per playlist item
2. **`--no-overwrites` + `--write-info-json`** — skip completed, cache metadata
3. **Limit quality** — `bestvideo[height<=1080]+bestaudio` avoids unnecessary 4K
4. **`--concurrent-fragments`** — speed up but throttle to avoid blocks

---

## Security

1. **Validate YouTube URLs** — regex allowlist: `(youtube\.com|youtu\.be)` only
2. **No arbitrary domains** — reject `file://`, localhost, internal IPs
3. **DMCA awareness** — 2026 ruling: third-party downloading as circumvention; personal use only
4. **Cookie files** — treat as secrets; never commit `cookies.txt`

---

## Related Projects (in workspace)

- **Python-projects** — shared Python CLI pattern and dependency hygiene
- **selenium_webdriver** — browser automation for JS-heavy sites

---

## Resources

| Resource | URL | Description |
|----------|-----|-------------|
| yt-dlp docs | https://github.com/yt-dlp/yt-dlp#readme | CLI documentation |
| curl_cffi | https://github.com/yifeikong/curl_cffi | TLS fingerprint library |
| FFmpeg Python | https://github.com/kkroening/ffmpeg-python | Python FFmpeg wrapper |
| YouTube scraping | https://dev.to/pickuma/yt-dlp-the-cli-video-downloader-developers-actually-use-in-2026-57jk | Method decision matrix |