# RESEARCH_REPORT.md

## Project: youtube-downloader

**Type:** YouTube CLI download tool
**Tech Stack:** Python 3.x, yt-dlp[curl-cffi], FFmpeg, ruff, mypy, uv, pytest
**Status:** Active

---

## Similar Projects

| Project | URL | Why Relevant |
|---------|-----|--------------|
| Python-projects | `projects/Python-projects` | Shared Python CLI + requirements hygiene |

---

## Key Findings

### yt-dlp + curl_cffi Best Practices (2026)
- **yt-dlp** is gold standard — 100K+ stars, 1,800+ sites, daily updates
- **Install `yt-dlp[curl-cffi]`** — `--impersonate chrome` bypasses bot protection
- **`--download-archive archive.txt`** — skip already-downloaded content; essential for cron jobs
- **`-o` output template** — `%(channel)s/%(upload_date)s_%(id)s.%(ext)s`; always include `%(id)s` to avoid title collisions
- **Cookie support** — `--cookies-from-browser firefox` for gated content
- **Format selector** — default `bv*+ba/b`; use `bv*[height<=1080]+ba*[ext=m4a]` for capped quality
- **Post-processing** — `--embed-metadata --embed-thumbnail --embed-subs --embed-chapters` in one pass

### curl_cffi for Bot Protection Bypass
- curl_cffi is a Python binding for curl-impersonate — mimics real browser TLS/JA3/HTTP2 fingerprints
- yt-dlp auto-uses curl_cffi when available for `--impersonate chrome`
- Key impersonation targets: `chrome`, `safari`, `safari_ios`, `firefox`, `edge`
- **Limitations**: beats TLS/HTTP2 fingerprinting; does NOT solve JavaScript challenges (Cloudflare Turnstile)

### Legal Landscape (2026)
- 2026 DMCA ruling: third-party downloading ruled as copyright circumvention; personal use only
- Creative Commons content explicitly downloadable — filter with `--match-filter "license!=*"`
- YouTube Premium offline download is the only legal method for copyrighted content
- Tool itself not infringing (RIAA vs youtube-dl 2020); distribution for infringing use is the risk

---

## Cheatsheets & Quick Reference

| Topic | Resource | Type |
|-------|----------|------|
| yt-dlp docs | <https://github.com/yt-dlp/yt-dlp> | Docs |
| curl_cffi | <https://github.com/yifeikong/curl_cffi> | Package |
| yt-dlp format selection | <https://github.com/yt-dlp/yt-dlp#format-selection> | Guide |

---

## Best Practices

1. **`--impersonate chrome`** — bypass bot protection via curl_cffi
2. **`--download-archive`** — skip duplicates; essential for automation
3. **Include `%(id)s` in output template** — avoid title collisions
4. **`--embed-metadata`** — embed all metadata in one pass
5. **FFmpeg post-processing** — set `--merge-output-format mp4` for consistent output

---

## Common Pitfalls

| Pitfall | Impact | Avoidance |
|--------|--------|-----------|
| No curl_cffi installed | Bot detection blocks | `pip install "yt-dlp[curl-cffi]"` |
| Missing `%(id)s` in output | Files overwritten | Always include `%(id)s` in template |
| No download archive | Repeated downloads | `--download-archive archive.txt` |
| Missing FFmpeg | Merge/subs fail | Install FFmpeg system-wide |

---

## Performance

1. **curl_cffi impersonation** — avoids bot-related rate limiting
2. **Format selection limiting** — cap quality to reduce download time and storage
3. **Download archive** — skip already-fetched content
4. **Concurrent downloads** — yt-dlp `--concurrent-fragments` for DASH streams
5. **Batch playlist mode** — single process for entire playlists

---

## Security

1. **No hardcoded cookies** — use `--cookies-from-browser` for authenticated access
2. **Validate output paths** — prevent path traversal via `..` in filenames
3. **Respect copyright** — personal use only; Creative Commons when possible
4. **FFmpeg from trusted source** — official builds only to avoid malware

---

## Related Projects (in workspace)

- **Python-projects** — shared Python CLI tooling patterns

---

## Resources

| Resource | URL | Description |
|----------|-----|-------------|
| yt-dlp GitHub | <https://github.com/yt-dlp/yt-dlp> | Download tool |
| curl_cffi | <https://github.com/yifeikong/curl_cffi> | TLS impersonation |
| yt-dlp format selection | <https://github.com/yt-dlp/yt-dlp#format-selection> | Format syntax |

### Research Methodology
- **Web search:** web_search (2026 yt-dlp patterns, legal landscape)
- **Documentation:** web_extract (yt-dlp, curl_cffi docs)
- **Legal research:** DMCA 2026 rulings on third-party downloading
- **Last verified:** 2026-07-16
