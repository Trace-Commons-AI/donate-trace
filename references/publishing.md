# Publishing to Trace Commons

## Where it goes
The dataset lives on the Hugging Face Hub. The cleaned session becomes one file in the dataset's folder tree:

```
sessions/<harness>/<filename>
```

where `<harness>` is one of `claude_code`, `codex`, `pi`, `opencode`, `cursor`. The session file is uploaded **raw and unmodified except for anonymization** — never reshaped or wrapped — so the Hub recognizes it as a native agent trace and renders the session timeline. All harnesses share a single dataset table; the folder name records the harness, so there is no per-agent config. Both submission paths below produce a pull request, never a direct push, so a maintainer reviews before anything becomes public.

The dataset is **`trace-commons/agent-traces`** and the anonymous ingestion
server is **`https://trace-commons-web.hf.space`** (the same Space that serves
the website; the donation endpoint is `/donate`). The license is **CC-BY-4.0** —
make sure the user understands the result is public under that license.

**CLI note.** The current Hugging Face CLI is `hf` (shipped with recent
`huggingface_hub`). Older machines have the deprecated `huggingface-cli` instead.
The commands below show `hf`; if it isn't found, fall back to the same command
with `huggingface-cli` (e.g. `huggingface-cli whoami`, `huggingface-cli upload`).
Detect with `command -v hf || command -v huggingface-cli`.

---

## Path A — attributed (user is logged in to Hugging Face)

The PR is opened under the user's own account. Use the CLI:

```bash
hf upload trace-commons/agent-traces \
  /tmp/donate-trace/cleaned.jsonl \
  sessions/<harness>/<filename> \
  --repo-type dataset \
  --create-pr
```

The command prints the pull request URL. Give it to the user.

---

## Path B — anonymous (no Hugging Face account)

The cleaned trace is sent to the Trace Commons server, which re-checks it and opens the PR under a project account. The user needs no Hugging Face login. The server is the same Space that hosts the website, at `https://trace-commons-web.hf.space`, so the donation endpoint is `https://trace-commons-web.hf.space/donate`.

```bash
curl -sS -X POST "https://trace-commons-web.hf.space/donate" \
  -H "Content-Type: application/json" \
  --data-binary @/tmp/donate-trace/payload.json
```

Build `payload.json` first so the trace is embedded safely as a JSON string:

```bash
python3 - <<'PY'
import json
trace = open('/tmp/donate-trace/cleaned.jsonl').read()
payload = {
    "harness": "<harness>",
    "filename": "<filename>",
    "consent": True,
    "trace": trace,
}
json.dump(payload, open('/tmp/donate-trace/payload.json', 'w'))
PY
```

- `consent: true` records that the user agreed to publish under the dataset's open license. Only set it after the user has confirmed.
- The server runs the same deterministic scrubber again as a backstop, then opens the PR. It returns JSON containing the pull request URL. Give that URL to the user.
- If the server rejects the submission (for example its backstop scrubber still finds a secret), it returns an error explaining what was found. Relay that to the user and do not retry blindly — clean the flagged item first.

---

## Consent and license
By submitting through either path, the contributor agrees the cleaned trace is published under the dataset's open license. For Path A, the user's own account action is the record. For Path B, the `consent` flag is the record. Either way, make sure the user understands the result is public and openly licensed before you submit. This ties back to the open-source-only rule.

## After submitting
Give the user the PR link so they can track it. Thank them once, briefly. Don't oversell or ask them to donate again.
