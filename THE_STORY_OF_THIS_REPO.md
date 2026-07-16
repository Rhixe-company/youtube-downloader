# The Story of This Repo — youtube-downloader

*A narrative built from real git data (5 commits, 2026-06-12 → 2026-07-16).*

## Year in Numbers
- **5** total commits (all within the last 12 months)
- **1** contributor — `rhixecompany <rhixecompany@gmail.com>`
- **29** tracked files (excluding `.git`/`node_modules`)
- **~228** lines of Python across 5 scripts
- **2** commit types used: `feat` (2), `chore` (2); 1 untyped
- **4** download modes: single, playlist, loop-single, loop-playlist

## Contributors
| Author | Commits | Share |
| --- | --- | --- |
| rhixecompany | 5 | 100% |

## Seasonal Patterns
- **2026-06** — 3 commits
- **2026-07** — 2 commits

Monthly research heartbeat, consistent with the whole workspace.

## Themes
- **Bootstrapping (Jun 12):** `chore: initial local project setup for youtube-downloader` — the four mode scripts landed together.
- **Open-source intent:** This is the only repo in the slice that ships a `LICENSE`, `CODE_OF_CONDUCT.md`, and GitHub `ISSUE_TEMPLATE`/`PULL_REQUEST_TEMPLATE` — signaling an intention to be a public, contributable project.
- **Research reporting:** `feat` commits (Jul 10, Jul 16) refresh `RESEARCH_REPORT.md` and add `web-research-youtube-downloader.md`.

## Plot Twists
1. **The most "finished" tool in the slice.** At ~228 lines across four purpose-built scripts plus `test.py`, it's a small, complete, runnable utility — unlike the larger apps that arrived as dormant specimens.
2. **Open-source costume, solo reality.** It wears full community scaffolding (LICENSE, CoC, PR template) yet has exactly one author and zero external commits. The welcome mat is out; no guests have arrived.
3. **curl_cffi as the secret sauce.** The choice of `curl_cffi` over plain `requests` is explicitly for bypassing bot protections — a quiet admission that this tool lives in an adversarial cat-and-mouse environment where YouTube's defenses must be worked around.

## Current Chapter
youtube-downloader is in **"complete utility, light maintenance"** mode. The code is done; recent commits only refresh research notes. The real risk to its future isn't bugs — it's YouTube/yt-dlp drift, since `AGENTS.md` itself warns to "keep yt-dlp updated for site compatibility." The next chapter is almost certainly a compatibility patch when YouTube changes something.

> Evidence note: figures from `git log`, `git shortlog -sne`, and file/LOC counts. Where history is silent, that silence is reported as fact.
