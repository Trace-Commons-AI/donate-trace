# opencode sessions

## The difference
Unlike the other agents, opencode does **not** store a session as one file. Its storage tree (`~/.local/share/opencode/storage/`) splits a session across `session/`, `message/`, and `part/` directories. Do not try to read those by hand.

## Use the export command instead
opencode can export one session as a single JSON document:

```bash
# find the session id
opencode session list --format json

# export it — ALWAYS use -o, never shell redirection (">")
opencode export <sessionID> --format json -o /tmp/donate-trace/opencode-session.json
```

Two known issues to handle:
1. **Never use `>` redirection.** A historical bug prepends a status line that breaks the JSON. Always use `-o`/`--output`.
2. **Version drift.** Older opencode versions emit pre-1.4 field shapes. After export, validate it parses as JSON before doing anything. If it won't parse, tell the user and stop.

## Format
`opencode export` produces opencode's own JSON document (a single object, not JSONL) containing the message history and metadata. The scrubber handles single-document JSON as well as JSONL.

Free-text carriers: message and part text fields within the exported document; working directory under the session metadata (`directory` / project path).

## Donating
opencode's representation in the dataset is not a settled convention yet — it is something this project defines. For now: after scrubbing the exported JSON, place it at `sessions/opencode/<sessionID>.json`. Flag to the user that opencode support is newer than the others.
