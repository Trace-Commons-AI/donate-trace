# opencode sessions

## The difference
Unlike the other agents, opencode does **not** store a session as one file. Its storage tree (`~/.local/share/opencode/storage/`) splits a session across `message/`, `part/`, `project/`, and `session_diff/` directories (the exact subdirs vary by version — on 1.1.x there is no top-level `session/` dir). Do not try to read those by hand.

## Use the export command instead
opencode can export one session as a single JSON document.

```bash
# find the session id (the --format json output includes id, title, directory)
opencode session list --format json
# session ids look like "ses_414f42d4effeu7crLsmVPtJhZd"

# export it (see the version note below for which form your CLI supports)
opencode export <sessionID> > /tmp/donate-trace/opencode-session.json
```

**CLI changed between versions — check what your `opencode export --help` accepts:**
- **Current opencode (verified on 1.1.4):** `export` takes only `[sessionID]`. There is **no `-o`/`--output` and no `--format` flag** — those are silently ignored and no file is written. You **must** capture stdout with `>` (or `opencode export <id> -o file` will produce nothing). On this version stdout is **clean** valid JSON (first byte `{`, last `}`) — the historical status-line-prepend bug is gone.
- **Older opencode:** some builds supported `--format json -o <file>` and/or prepended a status line to stdout. If your `export --help` shows `-o`/`--output`, prefer it.

**Always validate after export, on every version:** run the result through a JSON parser (`python3 -c "import json,sys;json.load(open(sys.argv[1]))" <file>`). If it won't parse — e.g. a leading status line from an old build — strip the offending line or tell the user and stop. Never scrub or donate a file that doesn't parse.

## Format
`opencode export` produces opencode's own JSON document (a single object, not JSONL) containing the message history and metadata. The scrubber handles single-document JSON as well as JSONL.

Free-text carriers: message and part text fields within the exported document; working directory under the session metadata (`directory` / project path).

## Donating
opencode's representation in the dataset is not a settled convention yet — it is something this project defines. For now: after scrubbing the exported JSON, place it at `sessions/opencode/<sessionID>.json`. Flag to the user that opencode support is newer than the others.
