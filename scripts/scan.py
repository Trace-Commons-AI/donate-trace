#!/usr/bin/env python3
"""
scan.py — optional deep secret scan for Trace Commons donations.

The deterministic scrubber (scrub.py) is a fast, high-confidence first pass with
a hand-maintained pattern list. This wraps TruffleHog (hundreds of maintained
detectors) for breadth — the same scanner the ingestion server runs as a
backstop. It is deliberately OPTIONAL:

  - If `trufflehog` is not installed, this prints a notice and exits cleanly.
    Nothing is required; the donation can still proceed on the scrub.py pass
    plus the human review. (The anonymous donation path also re-scans server
    side; attributed donations do not, which is exactly why running this
    locally is worthwhile.)
  - If it is installed, findings are reported for the review pass to confirm.
    They are NOT a hard block: TruffleHog runs WITHOUT verification (so no
    candidate secret is ever sent to a third party), which means it can
    false-positive on high-entropy strings (hashes, IDs, base64). Treat each
    finding as "confirm this isn't a real secret before uploading."

This mirrors the server's behaviour and flags; keep the two in sync.

Usage:
  python scan.py --in cleaned.jsonl [--report report.json]

Exit code is always 0 — this is advisory, not a gate. Read the STATUS line.
"""

import json
import shutil
import argparse
import subprocess


INSTALL_HINT = (
    "Install once (single static binary, no toolchain):\n"
    "  curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh "
    "| sh -s -- -b ~/.local/bin"
)


def scan(path):
    """Return (status, findings).

    status is one of: 'not_installed', 'clean', 'findings', 'error'.
    findings is a list of {detector, line, preview} dicts (empty unless 'findings').
    """
    if not shutil.which("trufflehog"):
        return "not_installed", []

    try:
        proc = subprocess.run(
            ["trufflehog", "filesystem", path,
             "--json", "--no-verification", "--no-update"],
            capture_output=True, text=True, timeout=180,
        )
    except (subprocess.TimeoutExpired, OSError):
        return "error", []

    findings = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        detector = obj.get("DetectorName") or obj.get("DetectorType")
        if not detector:
            continue
        raw = obj.get("Raw") or obj.get("RawV2") or ""
        preview = (raw[:4] + "…" + raw[-3:]) if len(raw) > 9 else "***"
        loc = (
            obj.get("SourceMetadata", {})
            .get("Data", {})
            .get("Filesystem", {})
            .get("line")
        )
        findings.append({"detector": str(detector), "line": loc, "preview": preview})

    return ("findings" if findings else "clean"), findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--report", default=None)
    args = ap.parse_args()

    status, findings = scan(args.inp)

    if status == "not_installed":
        print("STATUS: trufflehog_not_installed")
        print("Deep scan skipped — TruffleHog is not installed, so this donation")
        print("was checked by the pattern-based pass (scrub.py) only.")
        print("Anonymous donations are deep-scanned server-side; attributed ones")
        print("are not, so installing TruffleHog is worthwhile for attributed PRs.")
        print(INSTALL_HINT)
    elif status == "error":
        print("STATUS: scan_error")
        print("TruffleHog is installed but the scan did not complete (timeout or")
        print("execution error). Proceed on the scrub.py pass + review, or retry.")
    elif status == "clean":
        print("STATUS: clean")
        print("TruffleHog found no secrets in the cleaned trace.")
    else:  # findings
        detectors = sorted({f["detector"] for f in findings})
        print(f"STATUS: findings ({len(findings)})")
        print("Detectors: " + ", ".join(detectors))
        print("These ran WITHOUT verification and are often false positives on")
        print("high-entropy strings. Confirm each is NOT a real secret before upload:")
        for f in findings:
            loc = f"line {f['line']}" if f["line"] else "location unknown"
            print(f"  - {f['detector']}: {f['preview']} ({loc})")

    if args.report:
        with open(args.report, "w", encoding="utf-8") as f:
            json.dump({"status": status, "findings": findings}, f, indent=2)


if __name__ == "__main__":
    main()
