# pi sessions

## Location
`~/.pi/agent/sessions/`
Filenames look like `<timestamp>_<uuid>.jsonl` (some are just `<uuid>.jsonl`).

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
