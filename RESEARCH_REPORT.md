# RESEARCH_REPORT.md

## Project: youtube-downloader

**Type:** YouTube CLI download tool (pure CLI, no web UI)
**Tech Stack:** Python 3.11+ (recommended), yt-dlp[curl-cffi], FFmpeg, ruff, mypy
**Status:** Active
**Updated:** 2026-07-16

---

## 1. Project Overview

Python CLI tool using yt-dlp + curl_cffi for YouTube downloads (single, playlist, loop/batch). Pure CLI, no web UI. Uses the yt-dlp Python API directly. **Python 3.11 is now the recommended minimum** (yt-dlp 2026.07.04 raised the floor; 3.10 EOL Oct 2026).

## 2. yt-dlp Release Status (July 2026)

**Latest stable: 2026.07.04** (~178K+ GitHub stars). Verified changelog highlights: raise minimum Python to 3.11 (#17034); `--write-link` output now validated/escaped (CVE-2026-55404 fix); extractor fixes (bandcamp, linkedin, omnyfm, instagram, bilibili); `--exec` now restricts unsafe `%(...)s` conversions (use `%(...)q`). **Pin to `yt-dlp>=2026.07.04`** to cover all known July-2026 CVEs.

## 3. Security Vulnerabilities (Mid-2026 Cluster)

yt-dlp had 5+ CVEs since Feb 2026; all fixed in current stable:

| CVE | CVSS | Description | Fixed In |
|-----|------|-------------|----------|
| CVE-2026-55404 | 7.5 High | `--write-link` produces shortcut files with injected `file://` URIs — RCE when opened | 2026.07.04 |
| CVE-2026-50574 | 8.3 High | Unsanitized aria2c input via HLS/DASH manifests — RCE on Windows | 2026.06.09 |
| CVE-2026-50023 | 8.3 High | Bypass of CVE-2024-38519 — arbitrary OS-shortcut files | 2026.06.09 |
| CVE-2026-50019 | 6.1 Med | Cookie leak via curl redirects | 2026.06.09 |
| CVE-2026-26331 | 7.5 High | Command injection via `--netrc-cmd` | 2026.02.21 |

**Action:** Always `pip install -U yt-dlp`. Never use versions between 2026.02.21–2026.07.03 in production. Note: yt-dlp **deprecated Bun** as a runtime (supported only 1.2.11–1.3.14); use Python.

## 4. Bot Protection & 403 Fixes

**PO Token mismatch** (2026 issue): YouTube 403 errors when PO token client doesn't match download client. Fix: `--impersonate chrome --check-formats --rm-cache-dir` and force `player_client: ['web', 'web_safari']`. Deno may be needed for PO token generation. `curl_cffi` required for `--impersonate` — install `yt-dlp[curl-cffi]` (curl_cffi 0.15.x supported).

## 5. Best Practices

- **Format selectors** over numeric codes: `bv*[height<=1080]+ba/b`
- **`%(id)s`** in output template to prevent title collisions
- **`--download-archive archive.txt`** for idempotent runs
- **Embed all metadata in one pass** (FFmpegMetadata + EmbedThumbnail + EmbedSubtitle)
- **`--ignoreerrors`** for playlist pipelines
- **`--merge-output-format mp4`** for consistent output
- **`--concurrent-fragments 5`** (max 10) for DASH speed
- **`--sponsorblock-mark`** for built-in sponsor marking

## 6. Common Pitfalls

| Pitfall | Severity | Fix |
|---------|----------|-----|
| Numeric format codes in scripts | HIGH | `bv*[height<=1080]+ba/b` |
| Missing `%(id)s` in output template | HIGH | Add `%(id)s` to `outtmpl` |
| No `download_archive` | HIGH | Add `archive.txt` |
| No `impersonate` / curl_cffi | MEDIUM | Add player_client args |
| No `ignoreerrors` | MEDIUM | Add to playlist scripts |
| No rate limiting | MEDIUM | Add sleep/ratelimit options |

## 7. Similar Projects

| Project | Stars | Use Case |
|---------|-------|----------|
| yt-dlp | 178K+ | **Default choice** — active, 1800+ sites |
| youtube-dl | Stagnant | Legacy only |
| YouTube Data API v3 | — | Metadata/search (combo with yt-dlp) |
| tartube / Parabolic / Stacher | — | GUI wrappers around yt-dlp |

## 8. Performance Tips

- **Concurrent fragments:** 5 for DASH; >10 risks rate limits
- **aria2c:** `-x 16 -k 1M` for large files (but `--impersonate` won't apply)
- **Rate limit:** `--limit-rate 5M` prevents throttling
- **Cap quality:** 720p vs 4K = 5× less bandwidth
- **Archive:** O(1) set lookups, ~1.6MB for 70K entries
- **Batch:** one process per playlist; parallel processes for multi-video

## 9. Legal Landscape

2026 DMCA §1201 ruling classified third-party streaming downloads as copyright circumvention. Personal use has a narrow defense; Creative Commons explicitly permitted (`--match-filter "license!=*"`). YouTube Premium ($14/mo) is the only fully legal method for copyrighted offline viewing.

## 10. Resources

| Resource | URL |
|----------|-----|
| yt-dlp GitHub | https://github.com/yt-dlp/yt-dlp |
| Releases / Changelog | https://github.com/yt-dlp/yt-dlp/releases |
| Version history (videohelp) | https://www.videohelp.com/software/yt-dlp/version-history |
| Security advisories | https://github.com/yt-dlp/yt-dlp/security |
| curl_cffi | https://github.com/yifeikong/curl_cffi |
| Format selection | https://github.com/yt-dlp/yt-dlp#format-selection |

### Methodology
- 3 web searches (yt-dlp 2026.07.04, PO token 403 fixes, curl_cffi impersonate) + 1 web_extract verification (videohelp version history).
- **Last verified:** 2026-07-16.
