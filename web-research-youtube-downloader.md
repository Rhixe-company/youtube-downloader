# Web Research: youtube-downloader (Python + yt-dlp)

> **Generated:** 2026-07-16 | **Topic:** YouTube CLI Download Tool | **Stack:** Python 3.x, yt-dlp, curl_cffi, FFmpeg

---

## Table of Contents

1. [yt-dlp Best Practices (2026)](#1-yt-dlp-best-practices-2026)
2. [Similar Projects & Alternatives](#2-similar-projects--alternatives)
3. [Cheatsheets & Quick Reference](#3-cheatsheets--quick-reference)
4. [Common Pitfalls & How to Avoid Them](#4-common-pitfalls--how-to-avoid-them)
5. [Security Considerations](#5-security-considerations)
6. [Performance Tips](#6-performance-tips)
7. [Rate Limiting & Polite Scraping](#7-rate-limiting--polite-scraping)
8. [Python Packaging & CLI Tooling](#8-python-packaging--cli-tooling)
9. [Legal Landscape (2026)](#9-legal-landscape-2026)
10. [Codebase-Specific Findings](#10-codebase-specific-findings)
11. [Resources & References](#11-resources--references)

---

## 1. yt-dlp Best Practices (2026)

### 1.1 Always Use Format Selectors, Not Numeric Codes

**DO NOT** hard-code numeric format IDs (like `136`, `298`, `232`). YouTube reshuffles its format code list when it adds or deprecates encodings. Always use selector expressions:

```python
# ✅ Best practice — resolves at runtime
'format': 'bv*[height<=1080]+ba/b'

# ✅ MP4 container preferred
'format': 'bv*[ext=mp4]+ba*[ext=m4a]/b[ext=mp4]'

# ❌ Fragile — numeric codes break without warning
'format': '136+ba,298+ba,232+ba,bv+ba'  # Current project — BAD
```

**Key format selector syntax:**
- `bv*` / `ba*` — best video/audio with any codec
- `+` — merge separate video+audio streams
- `/b` — fallback to combined format if separate streams unavailable
- `[height<=1080]` — quality cap filter
- `[ext=mp4]` — container filter

### 1.2 Always Include `%(id)s` in Output Template

Video titles can collide. YouTube video IDs are unique. Without `%(id)s`, you risk silent file overwrites.

```python
# ✅ Safe — ID guarantees uniqueness
'outtmpl': 'downloads/%(uploader)s/%(upload_date)s_%(id)s.%(ext)s'

# ❌ Risky — two videos with same title = overwrite
'outtmpl': 'downloads/%(uploader)s/%(title)s.%(ext)s'  # Current project — RISKY
```

**Recommended template structure:**
```python
'outtmpl': 'downloads/%(channel)s/%(upload_date)s_%(id)s.%(ext)s'
```

### 1.3 Enable Download Archive for Idempotent Runs

`--download-archive archive.txt` (or `'download_archive': 'archive.txt'` in the Python API) appends each successfully downloaded video ID to a file. On subsequent runs, anything already in the archive is skipped. This is **the single most useful flag** for cron-driven mirroring of channels or playlists.

**Performance note (from Jody Bruchon's research):** With large archives (>70K entries), yt-dlp now reads the archive into a Python `set` at program startup rather than scanning the file per-video. This was a historic bottleneck that has been resolved since 2020 — performance is now O(1) for archive lookups.

### 1.4 Use curl_cffi with `--impersonate` for Bot Protection Bypass

```bash
pip install "yt-dlp[curl-cffi]"
```

Then in options:
```python
'extractor_args': {'youtube': {'player_client': ['web', 'web_safari']}},
```

Or via CLI:
```bash
yt-dlp --impersonate chrome ...
```

curl_cffi mimics real browser TLS/JA3/HTTP2 fingerprints, not just User-Agent. This beats TLS fingerprinting but does **NOT** solve JavaScript challenges (Cloudflare Turnstile).

**Available impersonation targets:** `chrome`, `safari`, `safari_ios`, `firefox`, `edge`

### 1.5 Embed All Metadata in One Pass

Rather than separate post-processing steps, combine them:

```python
'postprocessors': [
    {'key': 'FFmpegMetadata'},
    {'key': 'EmbedThumbnail', 'already_have_thumbnail': True},
    {'key': 'EmbedSubtitle'},
    {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'},
]
```

This is more efficient than running metadata embedding separately from format conversion.

### 1.6 Player Client Workaround

When YouTube changes its player and extraction breaks:
```python
'extractor_args': {'youtube': {'player_client': ['web', 'web_safari']}}
```

This forces specific clients when the default starts returning empty format lists. The yt-dlp issue tracker is the canonical place to find the current incantation when extraction breaks.

### 1.7 Use `ignoreerrors` for Batch/Playlist Downloads

For production pipelines, always include `'ignoreerrors': True` — otherwise one broken video in a playlist kills the entire run.

### 1.8 Pin yt-dlp Version in Production

For long-running pipelines, pin the yt-dlp version. The nightly channel is useful when you need a fresh extractor patch immediately, but breaks reproducibility. Lock to a stable release in production and rebuild dependencies weekly.

---

## 2. Similar Projects & Alternatives

### 2.1 Direct Alternatives to yt-dlp

| Project | Description | When to Use |
|---------|-------------|-------------|
| **yt-dlp** | Gold standard, 176K+ stars, 1,500+ contributors | Default choice for any download need |
| **youtube-dl** | Original project (stagnant since 2021) | Legacy scripts only — migrate to yt-dlp |
| **pytube** | Pure-Python YouTube downloader | Lightweight, no FFmpeg needed, but breaks frequently |
| **YouTube Data API v3** | Official Google API, quota-limited | Metadata-heavy workflows, search, channel analytics |
| **tartube** | GUI frontend for yt-dlp | Non-technical users, visual management |
| **yt-dlp-gui** | Cross-platform GUI (PySide6) | Users who want yt-dlp without CLI |
| **parabolic** | Modern Qt6 yt-dlp GUI | Linux desktop users |
| **stacher** | Electron-based yt-dlp GUI | Cross-platform GUI |
| **DownKingo** | Freeware with yt-dlp backend | One-click downloads with extra features |
| **4K Video Downloader** | Commercial ($25 lifetime) | Users who want polished paid experience |
| **ScreenApp** | Browser-based, AI features | Mobile/transcription needs |

### 2.2 Key Takeaway

**yt-dlp is the backbone of nearly every open-source video downloader in existence.** Projects like tartube, Parabolic, and Stacher are just GUIs wrapping yt-dlp. For a Python CLI tool, using yt-dlp directly (as this project does) is the correct approach.

### 2.3 Comparison: yt-dlp vs YouTube Data API

| Feature | yt-dlp | YouTube Data API |
|---------|--------|-----------------|
| Cost | Free | Free tier (10K quota/day) |
| Download video | ✅ Yes | ❌ No |
| Extract metadata | ✅ Rich (all page data) | ✅ Structured JSON |
| Rate limits | Soft (IP-based throttling) | Hard (quota caps) |
| Authentication | Cookie-based | OAuth 2.0 / API key |
| Maintainability | Active OSS | Google-maintained |
| Anti-bot bypass | curl_cffi impersonation | Official API (no bypass needed) |

**Recommendation:** For metadata-heavy projects, combine both — use YouTube Data API for initial search/discovery, then yt-dlp for actual downloading.

---

## 3. Cheatsheets & Quick Reference

### 3.1 Essential CLI Commands

```bash
# Basic download (best quality)
yt-dlp "URL"

# Best video+audio merged, MP4
yt-dlp -f "bv*+ba/b" --merge-output-format mp4 "URL"

# 1080p cap
yt-dlp -f "bv*[height<=1080]+ba/b" "URL"

# Audio only (MP3)
yt-dlp -x --audio-format mp3 --audio-quality 0 "URL"

# List available formats
yt-dlp -F "URL"

# Download specific formats by code
yt-dlp -f "137+140" "URL"

# Playlist with index in filename
yt-dlp -o "%(playlist_index)s - %(title)s.%(ext)s" "PLAYLIST_URL"

# Batch download from file
yt-dlp -a urls.txt

# Download archive (skip already downloaded)
yt-dlp --download-archive archive.txt --no-overwrites "PLAYLIST_URL"

# Custom output template
yt-dlp -o "~/Videos/%(upload_date>%Y-%m-%d)s - %(title)s [%(id)s].%(ext)s" "URL"

# Embed all metadata
yt-dlp --embed-metadata --embed-thumbnail --embed-subs "URL"

# Cookies from browser
yt-dlp --cookies-from-browser chrome "URL"

# Cookies from file
yt-dlp --cookies cookies.txt "URL"

# Rate limiting
yt-dlp --limit-rate 5M --sleep-interval 5 --max-sleep-interval 15 "URL"

# Concurrent fragments (faster DASH downloads)
yt-dlp --concurrent-fragments 5 "URL"

# External downloader for parallel segments
yt-dlp --external-downloader aria2c \
  --external-downloader-args "-x 16 -k 1M" "URL"

# Impersonate browser
yt-dlp --impersonate chrome "URL"

# Verbose debug
yt-dlp -vU "URL"

# Update yt-dlp
yt-dlp -U
```

### 3.2 Python API Quick Reference

```python
import yt_dlp
from yt_dlp.utils import DownloadError

# Basic download
ydl_opts = {
    'format': 'bv*+ba/b',
    'merge_output_format': 'mp4',
    'outtmpl': 'downloads/%(id)s.%(ext)s',
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=...'])

# Extract metadata without downloading
with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
    info = ydl.extract_info('URL', download=False)
    print(info['title'], info['duration'], info['uploader'])

# Audio extraction
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': '%(title)s.%(ext)s',
}

# Error handling
try:
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        ydl.download(['URL'])
except DownloadError as e:
    print(f"Download failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")

# Progress hooks
def my_hook(d):
    if d['status'] == 'downloading':
        print(f"Downloading: {d.get('_percent_str', 'N/A')}")
    elif d['status'] == 'finished':
        print("Download complete, processing...")

ydl_opts = {'progress_hooks': [my_hook]}
```

### 3.3 Output Template Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `%(id)s` | Video ID (unique) | `BaW_jenozKc` |
| `%(title)s` | Video title | `Rick Astley` |
| `%(ext)s` | File extension | `mp4` |
| `%(uploader)s` | Channel name | `RickAstleyVEVO` |
| `%(channel)s` | Channel name (alias) | `RickAstleyVEVO` |
| `%(upload_date)s` | Upload date (YYYYMMDD) | `20091025` |
| `%(upload_date>%Y-%m-%d)s` | Formatted date | `2009-10-25` |
| `%(playlist_title)s` | Playlist name | `Music Hits` |
| `%(playlist_index)s` | Position in playlist | `1` |
| `%(duration)s` | Duration in seconds | `212` |
| `%(view_count)s` | View count | `1234567890` |
| `%(like_count)s` | Like count | `12345` |
| `%(format)s` | Format description | `高清 1080p` |

**Filename safety:** Use `--restrict-filenames` (or `'restrictfilenames': True`) to replace special characters. Use `--trim-filenames N` to limit filename length on OS/filesystems with length constraints.

### 3.4 Format Selector Cheatsheet

| Expression | Description |
|------------|-------------|
| `bv*+ba/b` | **Default** — best video+audio, merge, fallback to combined |
| `bv*[height<=1080]+ba/b` | 1080p cap |
| `bv*[height<=1080]+ba*[ext=m4a]` | 1080p video + M4A audio |
| `bv*[ext=mp4]+ba*[ext=m4a]/b[ext=mp4]` | MP4 only |
| `bv*+ba` | Best of everything (no fallback) |
| `bestvideo+bestaudio` | Legacy syntax (still works) |
| `bestaudio/best` | Audio only |
| `m4a/bestaudio/best` | M4A preferred, then best audio |
| `bv*[vcodec^=avc1]+ba*[acodec^=mp4a]` | H.264 + AAC (max compatibility) |

---

## 4. Common Pitfalls & How to Avoid Them

### 4.1 Extractor Errors

**Symptom:** `ERROR: [youtube] ... unable to extract ...`

**Root cause:** YouTube updates its website structure, breaking yt-dlp's extractor.

**Fixes (in order):**
1. Update yt-dlp: `yt-dlp -U` (most common fix)
2. Clear cache: `yt-dlp --rm-cache-dir`
3. Try different player client: `--extractor-args "youtube:player_client=web,web_safari"`
4. Use nightly build: `pip install -U --pre yt-dlp`
5. Check yt-dlp issue tracker for known workarounds

### 4.2 HTTP 429: Too Many Requests

**Symptom:** Rate limiting from YouTube's servers.

**Fixes:**
- Add random sleep intervals: `--sleep-interval 5 --max-sleep-interval 15`
- Limit rate: `--limit-rate 5M`
- Lower concurrent fragments: `--concurrent-fragments 2`
- Use cookies from a logged-in browser (YouTube gives higher quota to authenticated users)
- Rotate IPs via proxy

### 4.3 HTTP 403: Forbidden

**Symptom:** Cloudflare/anti-bot blocking.

**Fixes:**
- Update yt-dlp
- Use `--impersonate chrome` (requires curl_cffi)
- Pass fresh cookies: `--cookies-from-browser firefox`
- Set correct User-Agent: `--user-agent "Mozilla/5.0..."`
- Refresh the target page in your browser within 30 min, then export cookies anew

### 4.4 FFmpeg Not Found / Merge Failures

**Symptom:** `ERROR: ffprobe/ffmpeg not found`, or downloaded video has no audio.

**Cause:** yt-dlp does not bundle FFmpeg. Most YouTube videos serve separate video and audio streams that must be merged.

**Fix:** Install FFmpeg and ensure it's on PATH.
- **Windows:** Place `ffmpeg.exe` in same folder as yt-dlp or add to PATH
- **macOS:** `brew install ffmpeg`
- **Linux:** `apt install ffmpeg`

**Important:** Do NOT install the Python package named `ffmpeg` — that's a different, unrelated project.

### 4.5 Filename Too Long

**Symptom:** `ERROR: unable to open for writing: [Errno 36] File name too long`

**Fix:** Truncate title in output template or use `--trim-filenames N`:
```python
'outtmpl': '%(uploader).30B - %(title).200B [%(id)s].%(ext)s'
```
Or:
```bash
yt-dlp --trim-filenames 100 "URL"
```

### 4.6 Numeric Format Codes Stop Working

**Symptom:** `ERROR: requested format not available`

**Cause:** YouTube rotates numeric format IDs. `136` (h264-720p), `298` (h264-720p60), `137` (h264-1080p), etc. are not guaranteed to exist tomorrow.

**Fix:** Switch to format selectors (see §1.1).

### 4.7 File Already Exists / Overwrite Issues

**Symptom:** Files being silently overwritten or skipped unexpectedly.

**Fixes:**
- Always include `%(id)s` in output template to prevent collision
- Use `--no-overwrites` to skip existing files
- Use `--download-archive archive.txt` for robust deduplication
- Use `--force-overwrites` if you want to replace files intentionally

### 4.8 Age-Restricted Content

**Symptom:** `ERROR: Sign in to confirm your age`

**Fix:** Pass cookies from a logged-in browser:
```python
'cookiefile': 'cookies.txt'  # exported cookies in Netscape format
```
or from CLI: `--cookies-from-browser chrome`

### 4.9 livestream Downloads

For live streams, use `--live-from-start` to capture from the beginning:
```bash
yt-dlp --live-from-start "URL"
```
Use `--hls-use-mpegts` for corrupted-stream recovery.

### 4.10 SponsorBlock Integration

yt-dlp has built-in SponsorBlock support:
```bash
# Mark sponsor segments
yt-dlp --sponsorblock-mark all "URL"

# Remove sponsor segments (requires re-encode)
yt-dlp --sponsorblock-remove all "URL"

# Available categories: sponsor, intro, outro, selfpromo, preview, interaction, music_offtopic
```

---

## 5. Security Considerations

### 5.1 CRITICAL: CVE-2026-50574 & CVE-2026-50023 (June 2026)

**Severity: CRITICAL (CVSS 9.6)**

Two vulnerabilities were patched in yt-dlp 2026.06.09:

| CVE | Description | Impact |
|-----|-------------|--------|
| **CVE-2026-50574** | Insufficiently sanitized input passed to aria2c allows arbitrary file write via fragmented manifests (HLS/DASH) | **Windows:** Immediate RCE. **Non-Windows:** RCE on next yt-dlp invocation |
| **CVE-2026-50023** | Bypass of CVE-2024-38519 fix — arbitrary OS-shortcut files (.desktop, .url, .webloc) can be written | Arbitrary code execution |

**Mitigation:** `pip install -U yt-dlp>=2026.6.9`

### 5.2 CVE-2024-38519: Path Traversal via Filename Injection (2024)

**Severity: HIGH (CVSS 7.8)**

yt-dlp did not limit extensions of downloaded files. An attacker could craft a video title like:
- `ffmpeg.exe` → overwrites ffmpeg.exe in working directory
- `yt-dlp.conf` → creates malicious config in working directory

**Fixed in:** yt-dlp 2024.07.01

**Precautions:**
- ✅ **Always** have `.%(ext)s` at the end of your output template
- ✅ Restrict filenames: `--restrict-filenames` or `'restrictfilenames': True`
- ✅ Keep yt-dlp updated
- ✅ Download to a dedicated directory (never the yt-dlp install directory)
- ✅ Validate URLs before passing to yt-dlp

### 5.3 Cookie Security

- Cookies exported from browser contain **all** site cookies, not just YouTube
- Never commit cookie files to VCS
- Use `--cookies-from-browser` over exporting cookies to a file when possible
- Rotate cookies regularly if using a shared cookie file

### 5.4 General Security Best Practices

| Practice | Why |
|----------|-----|
| Use `--restrict-filenames` | Prevents path traversal & special char injection |
| Keep yt-dlp updated | Latest security patches |
| Validate input URLs | Prevent SSRF via crafted URLs |
| Don't run as root/admin | Limit blast radius of potential exploits |
| Install FFmpeg from official source | Third-party FFmpeg builds can contain malware |
| Scan downloaded content | External video files could theoretically contain exploits |
| Use `pipx` or venv | Isolate yt-dlp and its dependencies from system Python |
| Pin or version-lock yt-dlp | Avoid surprise security regressions from auto-updates |

### 5.5 Cookie File Export Warning (from yt-dlp FAQ)

Using `yt-dlp --cookies-from-browser chrome --cookies cookies.txt` exports **ALL** browser cookies for **ALL** sites, not just the requested video. Handle the resulting file with extreme care — it's equivalent to handing over your browser session.

---

## 6. Performance Tips

### 6.1 Concurrent Fragment Downloads

For DASH streams (YouTube splits videos into many small fragments):
```python
'concurrent_fragments': 5  # default in yt-dlp
```
Or CLI: `--concurrent-fragments 5`

**Caveats:**
- Too high (>10) can trigger rate limiting from a single IP
- Uses more memory (fragments buffered before merging)
- The `-N` option on CLI controls this

### 6.2 External Downloaders

For large files or unstable connections, use aria2c as external downloader:
```bash
yt-dlp --external-downloader aria2c \
  --external-downloader-args "-x 16 -k 1M" "URL"
```
- `-x 16` = 16 connections per file
- `-k 1M` = 1 MB segment size

**Caveat:** This uses aria2c's own network stack, not yt-dlp's, so features like `--impersonate` won't apply to aria2c connections.

### 6.3 Limit Download Speed

Prevent saturating your connection and triggering throttles:
```python
'ratelimit': 5 * 1024 * 1024  # 5 MB/s in bytes
```
Or CLI: `--limit-rate 5M`

### 6.4 Metadata-Only Extraction (Skip Download)

When you only need info (titles, durations, format lists):
```python
'skip_download': True,
'writeinfojson': True,  # writes .info.json alongside
```

### 6.5 Archive File Performance

With large archive files (50K+ entries):
- yt-dlp now loads the entire archive into a Python `set` at startup
- This makes lookups O(1) (constant time)
- Memory overhead is negligible (~1.6 MB for 70K entries)

### 6.6 Batch vs Sequential Playlist Downloads

- **Single playlist:** yt-dlp processes items sequentially within one process
- **Multiple URLs:** yt-dlp can accept multiple URLs in one command
- **Multiple playlists:** Use `--batch-file` or a loop in Python
- **Parallel downloads:** Consider running multiple yt-dlp processes in parallel for different videos (each on its own)

### 6.7 Format Selection for Performance

- Downloading 720p vs 4K uses ~5x less bandwidth and storage
- Audio-only downloads use minimal bandwidth
- Use `--merge-output-format mp4` to avoid unnecessary re-encoding
- `--recode-video` re-encodes (slow, CPU-intensive) — avoid unless needed

### 6.8 Speed Comparison (From Real-World Benchmarks)

| Scenario | Time |
|----------|------|
| Single 10-min 1080p video (basic) | ~30-60 seconds |
| Playlist of 50 shorts (metadata only) | ~2-3 minutes |
| 600-video channel (metadata + subs only) | ~40 minutes |
| Single 4K HDR video | ~5-15 minutes (depends on connection) |
| Channel archive with 70K archive entries (check skip) | ~17 comparisons (vs 70K with old code) |

---

## 7. Rate Limiting & Polite Scraping

### 7.1 yt-dlp Rate Limiting Options

```python
'sleep_interval': 5,          # seconds between downloads
'max_sleep_interval': 15,     # randomize up to this
'sleep_interval_requests': 1,  # seconds between HTTP requests during extraction
'ratelimit': 5 * 1024 * 1024,  # 5 MB/s bandwidth cap
'concurrent_fragments': 3,    # lower = less aggressive
'retries': 10,                # retry on failure
'fragment_retries': 10,       # retry individual fragments
'skip_unavailable_fragments': True,  # skip broken fragments
```

### 7.2 Recommended Settings for Unattended Jobs

```python
ydl_opts = {
    'sleep_interval': 5,
    'max_sleep_interval': 15,
    'sleep_interval_requests': 1,
    'ratelimit': 5 * 1024 * 1024,  # 5 MB/s
    'concurrent_fragments': 3,
    'retries': 10,
    'fragment_retries': 10,
    'ignoreerrors': True,
}
```

### 7.3 Handling 429 Errors

- **Immediate:** Add sleep intervals and reduce rate
- **Proactive:** Use cookies (authenticated users get higher quotas)
- **Scale:** Rotate residential proxies for heavy use
- **Retry strategy:** Implement exponential backoff in your wrapper
- **Long-term:** For commercial/bulk use, consider a paid scraping service or YouTube Data API

### 7.4 Multi-IP / Proxy Rotation

For large-scale operations, yt-dlp supports proxies:
```python
'proxy': 'socks5://user:pass@host:1080'
```

Residential proxy networks (Bright Data, Oxylabs, etc.) provide undetectable IP rotation but are expensive.

---

## 8. Python Packaging & CLI Tooling

### 8.1 Modern Python Tooling (2026)

| Tool | Role | Recommendation |
|------|------|----------------|
| **uv** | Package manager (Rust) | Replace pip+venv+poetry, 10-100x faster |
| **pipx** | CLI tool installer | Install yt-dlp as an isolated CLI |
| **ruff** | Linter + formatter | Replace black+flake8+isort (800+ rules, ms runtime) |
| **mypy** strict | Type checker | Production baseline for Python |
| **pytest** | Test framework | Already in requirements/local.txt ✅ |

### 8.2 Best Practices for yt-dlp CLI Projects

1. **Use a virtual environment** — `uv venv` or `python -m venv`
2. **Install yt-dlp[curl-cffi]** — essential for bypassing bot protection:
   ```bash
   pip install "yt-dlp[default,curl-cffi]"
   ```
3. **Pin dependencies** (`uv lock` or `pip freeze > requirements.txt`)
4. **Use `pipx` for end-user installation** — isolates dependencies globally
5. **Configuration file** — yt-dlp reads `~/.yt-dlp/config` or `yt-dlp.conf` in working dir for default options

### 8.3 PEP 723 Inline Script Metadata (2026)

For single-file scripts (like the existing `main_noplaylist.py`), PEP 723 allows embedding metadata:
```python
# /// script
# dependencies = [
#   "yt-dlp[default,curl-cffi]",
# ]
# ///
```

This lets `uv run main_noplaylist.py` automatically create an environment.

### 8.4 requirements/ Structure Analysis

The current project uses a `requirements/` directory with:
- `base.txt` — generic Python tooling (sphinx, black, ruff, etc.)
- `local.txt` — extends base.txt with `-r ./base.txt`, adds mypy, pytest, yt-dlp[curl-cffi]

**Issues:**
- `base.txt` contains purely dev/build dependencies (sphinx, djlint, etc.) — not "base" at all
- The only actual runtime dependency (`yt-dlp[curl-cffi]`) is tucked in `local.txt`
- No `production.txt` for runtime-only deps

**Recommendation:** Restructure as:
```
requirements/
├── runtime.txt     # yt-dlp[curl-cffi], certifi, etc.
├── dev.txt         # pytest, mypy, ruff, pre-commit
└── docs.txt        # sphinx, sphinx-autobuild
```

---

## 9. Legal Landscape (2026)

### 9.1 DMCA Anti-Circumvention Ruling

A 2026 DMCA §1201 ruling classified third-party downloading of streamed content as copyright circumvention. Key implications:
- **Personal use** has a narrow legal defense but is not explicitly protected
- **Commercial use** of downloaded copyrighted content is clearly infringement
- **Tool distribution** is risky — RIAA vs youtube-dl (2020) established that the tool itself isn't infringing, but distributing it with the intent of facilitating infringement is

### 9.2 Safe Practices

| Practice | Status |
|----------|--------|
| Downloading your own uploaded content | ✅ Likely safe (you hold the copyright) |
| Downloading Creative Commons content | ✅ Explicitly permitted |
| Downloading public domain content | ✅ No restrictions |
| Personal archive of family/friends | ⚠️ Gray area |
| Commercial training data from others' videos | ❌ High risk |
| Redistributing downloaded copyrighted content | ❌ Clear infringement |
| Building a paid service around yt-dlp | ❌ High legal risk |

### 9.3 Filtering for Creative Commons

```python
--match-filter "license!=*"  # Skip videos without license info
```

This filters to only videos that have a known license (which is usually Creative Commons).

### 9.4 YouTube Premium Alternative

YouTube Premium ($14/mo) provides official offline downloads, no ads, and YouTube Music. It's the only 100% legal method for downloading copyrighted YouTube content for offline viewing.

---

## 10. Codebase-Specific Findings

Review of the existing `projects/youtube-downloader` code against research findings.

### 10.1 Current Issues Found

| Issue | Files Affected | Severity | Fix |
|-------|---------------|----------|-----|
| Hardcoded numeric format codes | All 4 main scripts | **HIGH** | Switch to format selectors |
| Missing `%(id)s` in output template | All 4 main scripts | **HIGH** | Add `%(id)s` |
| No download archive | All scripts | **HIGH** | Add `download_archive` |
| No curl_cffi impersonation | All scripts | **MEDIUM** | Add `impersonate` option |
| No error handling (`ignoreerrors`) | main_noplaylist.py, main_playlist.py | **MEDIUM** | Add `ignoreerrors: True` |
| MKV output (still valid but less compatible) | All except test.py | **LOW** | Consider MP4 default |
| No cookie support | All scripts | **MEDIUM** | Add `cookiefile` option |
| No rate limiting | All scripts | **MEDIUM** | Add sleep intervals |
| Embedded test URLs in code | All scripts | **LOW** | Move to config/env/input |
| No config file support | All scripts | **LOW** | Add yt-dlp config or project config |
| requirements/base.txt polluted with dev deps | requirements/base.txt | **LOW** | Split runtime/dev properly |

### 10.2 What's Working Well

- ✅ Using yt-dlp Python API (not subprocess)
- ✅ `writethumbnail` and `writesubtitles` enabled
- ✅ Subtitle embedding configured
- ✅ Separate scripts for different modes (single, playlist, loop)
- ✅ Test file exists (test.py)
- ✅ `yt-dlp[curl-cffi]` in requirements

### 10.3 Quick Wins (Low Effort, High Impact)

1. **Change format to selector** in all files:
   ```python
   'format': 'bv*[height<=1080]+ba/b',
   ```

2. **Add `%(id)s` to output template** in all files:
   ```python
   'outtmpl': 'downloads/%(uploader)s/%(title)s [%(id)s].%(ext)s',
   ```

3. **Add download archive** to prevent re-downloads:
   ```python
   'download_archive': 'archive.txt',
   ```

4. **Add `ignoreerrors: True`** to playlist/loop scripts

5. **Add sleep intervals** for polite downloading

---

## 11. Resources & References

### Official Documentation

| Resource | URL |
|----------|-----|
| yt-dlp GitHub | https://github.com/yt-dlp/yt-dlp |
| yt-dlp README (full options) | https://github.com/yt-dlp/yt-dlp#readme |
| yt-dlp Python API | https://github.com/yt-dlp/yt-dlp#embedding-yt-dlp |
| yt-dlp Format Selection | https://github.com/yt-dlp/yt-dlp#format-selection |
| yt-dlp Output Template | https://github.com/yt-dlp/yt-dlp#output-template |
| yt-dlp Configuration | https://github.com/yt-dlp/yt-dlp#configuration |
| yt-dlp FAQ | https://github.com/yt-dlp/yt-dlp/wiki/FAQ |
| yt-dlp Post-Processing | https://github.com/yt-dlp/yt-dlp#post-processing |
| curl_cffi | https://github.com/yifeikong/curl_cffi |
| FFmpeg | https://ffmpeg.org/ |
| uv (Python package manager) | https://docs.astral.sh/uv/ |
| pipx | https://pypa.github.io/pipx/ |
| ruff (linter) | https://docs.astral.sh/ruff/ |

### Cheatsheets & Guides

| Resource | URL |
|----------|-----|
| yt-dlp Cheat Sheet (ditig.com) | https://www.ditig.com/yt-dlp-cheat-sheet |
| yt-dlp Man Page (mankier.com) | https://www.mankier.com/1/yt-dlp |
| yt-dlp Troubleshooting | https://yt-dlpc.github.io/troubleshooting.html |
| Complete yt-dlp Tutorial (ostechnix) | https://ostechnix.com/yt-dlp-tutorial/ |
| yt-dlp in 2026 Guide (dev.to) | https://dev.to/pickuma/yt-dlp-the-cli-video-downloader-developers-actually-use-in-2026-57jk |

### Security Advisories

| Advisory | URL |
|----------|-----|
| CVE-2026-50574 (Critical) | https://security-tracker.debian.org/tracker/CVE-2026-50574 |
| CVE-2026-50023 (Critical) | https://github.com/yt-dlp/yt-dlp/security/advisories/GHSA-c6mh-fpjc-4pr3 |
| CVE-2024-38519 (High) | https://github.com/advisories/GHSA-79w7-vh3h-8g4j |
| yt-dlp Security Advisories | https://github.com/yt-dlp/yt-dlp/security/advisories |
| Tenable Plugin 321527 | https://www.tenable.com/plugins/nessus/321527 |

### Similar Projects

| Project | URL |
|---------|-----|
| tartube (GUI) | https://github.com/axcore/tartube |
| yt-dlp-gui | https://github.com/oleksis/yt-dlp-gui |
| Parabolic | https://github.com/NickvisionApps/Parabolic |
| Stacher | https://stacher.io |
| 4K Video Downloader | https://www.4kdownload.com/products/videodownloader |

### Wrapper Examples

| Resource | URL |
|----------|-----|
| alexwlchan/yt-dlp_alexwlchan | https://github.com/alexwlchan/yt-dlp_alexwlchan |
| yt-dlp with Python + Proxy (Medium) | https://medium.com/@datajournal/supercharge-yt-dlp-with-python-geo-bypass-batch-downloads-proxy-rotation-06ab36f15f76 |
| Things learned building a yt-dlp wrapper | https://arkadiuszchmura.com/posts/things-i-learned-while-building-a-yt-dlp-wrapper |

### Legal Resources

| Resource | URL |
|----------|-----|
| YouTube Terms of Service | https://www.youtube.com/t/terms |
| Creative Commons on YouTube | https://support.google.com/youtube/answer/2797468 |
| DMCA §1201 | https://www.copyright.gov/title17/92chap12.html |
| RIAA vs youtube-dl (2020) | https://github.com/github/dmca/blob/master/2020/11/2020-11-06-RIAA.md |

---

## Research Methodology

- **Web search:** `web_search` (10 queries across 4 batches)
- **Documentation:** `web_extract` (yt-dlp README, FAQ, cheat sheet, man page, blog posts)
- **Vulnerability research:** CVE databases (Tenable, Debian tracker, GitHub Advisories)
- **Codebase analysis:** Existing 4 Python scripts, requirements/, test.py, README.md
- **Last verified:** 2026-07-16

## Sources Used

1. dev.to — yt-dlp: The CLI Video Downloader Developers Actually Use in 2026
2. yt-dlp GitHub — README, Wiki/FAQ, Format Selection docs
3. ditig.com — yt-dlp Cheat Sheet
4. mankier.com — yt-dlp Man Page
5. medium.com/@datajournal — yt-dlp + Python: Geo-Bypass & Proxy Rotation
6. alexwlchan.net — Creating a personal wrapper around yt-dlp
7. jodybruchon.com — youtube-dl archive performance optimization (historical)
8. Tenable, Debian, GitHub Advisories — CVE-2026-50574, CVE-2024-38519
9. reddit.com/r/youtubedl — Community discussions on pitfalls & best practices
10. roundproxies.com — yt-dlp step-by-step guide 2026
11. downkingo.com — Open source video downloaders comparison 2026
12. screenapp.io — Best YouTube downloaders 2026
13. packaging.python.org — Standalone CLI tool installation
14. tech-insider.org — uv vs pip comparison 2026
