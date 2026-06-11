# Codex sessions

## Location
`~/.codex/sessions/` (and `~/.codex/archived_sessions/`)
Filenames look like `rollout-<timestamp>-<uuid>.jsonl`.

One JSONL file per session. Pick the most recently modified unless the user names one.

## Format
One JSON object per line. Top-level `type` is one of: `response_item`, `event_msg`, `session_meta`, `turn_context`. Almost everything is wrapped in a `payload` object.

Identity / sensitive fields:
- `payload.cwd` — working directory (contains the username)
- `payload.id` — session id

Free-text carriers:
- `payload.content[].text` — both input (`input_text`) and output (`output_text`) prose
- any command/tool payloads under `payload` — inspect for shell commands

## Donating
Native file is the right shape. After scrubbing, place at `sessions/codex/<filename>`.
