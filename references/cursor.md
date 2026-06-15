# Cursor sessions

Cursor support is newer than the others — flag that to the user. The paths below come from Cursor's documented storage layout, not yet a verified live donation; sanity-check what's actually on disk before trusting them, and prefer the most recently modified file.

## Location
The Cursor CLI agent (`cursor-agent`, often aliased `agent`) writes a **JSONL transcript per session** — this is the right shape to donate:

`~/.cursor/projects/<project>/agent-transcripts/<id>.jsonl`

Find the newest with a recursive search rather than a flat `ls`:
`find ~/.cursor/projects -path '*/agent-transcripts/*.jsonl' -print0 | xargs -0 ls -t | head -1`

Cursor also keeps chat **metadata** in SQLite (`~/.cursor/chats/*/*/store.db`) and the desktop app stores composer/chat state inside `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb` (Linux: `~/.config/Cursor/...`). **Do not** try to read those by hand — donate the `agent-transcripts/*.jsonl` file, which is already one clean line-per-event document.

To list/resume sessions from the CLI: `cursor-agent ls` and `cursor-agent --resume <id>`.

## Format
One JSON object per line (JSONL). The scrubber handles JSONL directly. Identity / free-text carriers to expect (the deterministic scrubber walks every string value regardless, so this is mainly for the Step 4 review pass):
- a working-directory / project-path field (contains the username) — redacted by the home-path rule
- prompt and assistant message text, and any shell-command / tool-call payloads — inspect for names, internal hostnames, secrets a regex can't catch

## Donating
Native transcript file is the right shape. After scrubbing, place at `sessions/cursor/<filename>`.
