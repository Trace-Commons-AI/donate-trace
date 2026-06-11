# pi sessions

## Location
`~/.pi/agent/sessions/` — sessions are **grouped into one subdirectory per project**,
named after the slugified working directory, not stored flat. The real layout is:
`~/.pi/agent/sessions/<project-slug>/<timestamp>_<uuid>.jsonl`
(e.g. `~/.pi/agent/sessions/--Users-USER-ComparIA--/2026-04-29T15-34-56-687Z_<uuid>.jsonl`).
Verified against a real install. Filenames are `<ISO-timestamp>Z_<uuid>.jsonl`.

Recurse to find the latest, e.g.
`find ~/.pi/agent/sessions -name '*.jsonl' -print0 | xargs -0 ls -t | head -1`.

One JSONL file per session. Pick the most recently modified unless the user names one.

## Format
One JSON object per line. Top-level `type` is one of: `message`, `session`, `model_change`, `thinking_level_change`, `compaction`.

Identity / sensitive fields:
- top-level `cwd` — working directory (contains the username)
- top-level `id`, `version`

Free-text carriers:
- `message.content` — either a string or a list of blocks; when a list, each block may have `.text`
- inspect message content for shell commands and tool output

## Donating
Native file is the right shape. After scrubbing, place at `sessions/pi/<filename>`.

## Note
pi invokes the skill as `/skill:donate-trace` rather than `/donate-trace`.
