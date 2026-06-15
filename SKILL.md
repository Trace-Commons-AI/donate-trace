---
name: donate-trace
description: Donate a single coding-agent session to Trace Commons, an open public dataset of agent traces. Use this skill whenever the user wants to donate, contribute, share, or publish an agent session, trace, or conversation history to Trace Commons or an open dataset, or says things like "/donate-trace", "donate this session", "contribute my trace", "share this to the commons", or "publish my agent history". The skill locates the current session from the agent's own logs, strips paths, identity, secrets and PII locally, shows the user exactly what was removed, confirms the project is open-source, and opens a pull request to the dataset. Only ever donates from public, open-source repositories — never private or proprietary code.
---

# Donate a trace to Trace Commons

Trace Commons is one open, public dataset of coding-agent sessions that anyone can train on or study. This skill takes a single session from the current agent, removes anything sensitive on the user's own machine, and submits the cleaned result as a pull request to the dataset.

The whole point is that contributing is safe and the user stays in control: nothing leaves the machine until the user has seen what will be sent and confirmed it. Treat that promise as the core of the job.

## Hard rules (read first)

These are not negotiable. The dataset is public and permanent, so a mistake here is published immediately.

1. **Open-source only.** Donate a session only if the project is a public, openly-licensed repository. If you cannot confirm the repo is public, stop and ask. Never donate sessions from private, proprietary, work, or client code. If the user can't confirm it's public and open-source, do not proceed.
2. **Local cleaning before upload.** All anonymization happens on this machine, before anything is sent. Never upload a raw session.
3. **User reviews before send.** Always show the user a summary of what was removed and ask for explicit confirmation. No silent uploads.
4. **One session only.** Donate the single session the user chose, not their whole history.
5. **If something looks wrong, stop.** If you're unsure whether a field is sensitive, redact it. If you're unsure whether the repo is public, ask. Dropping signal is acceptable; leaking is not.

## The flow

Follow these steps in order.

### Step 1 — Confirm it's open-source

Before touching any logs, confirm the project the session came from is a public, open-source repository.

- If you can see the working directory, check whether it has a git remote pointing at a public host and an open-source license. Run `git -C <dir> remote get-url origin` and `git -C <dir> config --get remote.origin.url` to find the remote, and look for a LICENSE file.
- Even if it looks public, ask the user to confirm in plain language: "I'll donate this session to the public Trace Commons dataset. Can you confirm this project is open-source and public? I won't proceed otherwise."
- If they can't confirm, stop here and explain why.

### Step 2 — Find the session

Identify which agent (harness) this is and locate the session file. Each agent stores sessions differently. Read the matching reference file for exact paths and formats:

- **Claude Code** → `references/claude-code.md`
- **Codex** → `references/codex.md`
- **pi** → `references/pi.md`
- **opencode** → `references/opencode.md`
- **Cursor** → `references/cursor.md`

If you're not sure which agent you're running in, ask the user, or infer it from which session directory exists on disk. Default to the most recently modified session unless the user names a specific one.

Copy the session to a working location (e.g. `/tmp/donate-trace/`) so you never modify the user's real logs.

### Step 3 — Clean it (deterministic pass first)

Run the bundled scrubber on the copied file. It removes the highest-confidence leaks deterministically — home-directory paths and usernames, common secret formats (API keys, tokens, PEM blocks, JWTs, `KEY=value` env assignments in shell commands), and emails. Doing these in code rather than by eye is deliberate: these patterns have crisp signatures and a missed credential is the worst outcome.

```bash
python scripts/scrub.py --in /tmp/donate-trace/<session-file> --harness <harness> --out /tmp/donate-trace/cleaned.jsonl --report /tmp/donate-trace/report.json
```

The scrubber writes the cleaned session and a JSON report listing every redaction it made.

### Step 4 — Review pass (your judgment)

The scrubber catches patterns; you catch meaning. Read the cleaned session and look for things a regex can't recognize:

- Personal names, company names, or client names in prose (prompts, commit messages, comments).
- Internal hostnames, project codenames, ticket IDs, or URLs that identify a person or org.
- Anything in free text that a stranger could use to identify who wrote this or where they work.

Redact anything you find by replacing it with a neutral placeholder (e.g. `[NAME]`, `[COMPANY]`, `[INTERNAL_URL]`). Note what you changed so it can go in the summary. When unsure, redact.

See `references/anonymization.md` for the full field-by-field guide to where sensitive data hides in each harness.

### Step 5 — Show the user, get confirmation

Summarize plainly what will be donated and what was removed. Keep it human:

```
Ready to donate this session to Trace Commons.

Removed:
- 4 home-directory paths (your username)
- 1 API key in a shell command
- 2 email addresses
- 1 company name in a commit message ("Acme")

The cleaned session has 35 messages and 12 tool calls. Nothing has been
uploaded yet. Want me to open the pull request?
```

Wait for explicit confirmation. If the user wants to see the full cleaned file, show it. If they want to pull something else out, do it and re-summarize.

### Step 6 — Submit

Only after confirmation. There are two ways to submit, and the skill picks one automatically but lets the user choose.

First, detect whether this machine has a Hugging Face login. The current CLI is
`hf`; older machines have the deprecated `huggingface-cli`. Use whichever exists:

```bash
HF_CLI=$(command -v hf || command -v huggingface-cli)
"$HF_CLI" auth whoami 2>/dev/null || "$HF_CLI" whoami 2>/dev/null
```

(`hf auth whoami` is the current form; the legacy CLI uses `huggingface-cli whoami`.)

- **If it succeeds** (prints a username): default to the **attributed** path. The donation becomes a pull request opened by the user's own account. Tell them: "You're logged in to Hugging Face as `<name>`, so I'll open the pull request under your account. Prefer to donate anonymously instead?"
- **If it fails** (not logged in): default to the **anonymous** path. The donation is sent through the Trace Commons server, which opens the pull request on your behalf under a project account. No Hugging Face account needed. Tell them: "You're not logged in to Hugging Face, so I'll donate anonymously through the Trace Commons server. Prefer to attribute it to your own account? You'd need to run `hf auth login` (or `huggingface-cli login` on older installs) first."

Always state which path you're taking and let the user switch. Some people want attribution; some specifically want anonymity even when logged in. Respect the override.

Then submit via the chosen path. Both paths open a pull request (never a direct push) so a maintainer reviews before anything goes public. See `references/publishing.md` for the exact commands for each path.

Then tell the user where to track it and thank them once, briefly.

## If the user just wants to understand the skill

If they're asking what this does rather than asking to donate right now, explain it plainly and point them at the open-source-only rule. Don't start reading their logs unless they want to donate.
