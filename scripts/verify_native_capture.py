#!/usr/bin/env python3
"""Read actual stored native evidence, optionally uploaded and hosted identities.

Raw transcripts are inspected in memory and hashed, never printed or copied.
"""
import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def run(argv, cwd):
    result = subprocess.run(argv, cwd=cwd, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(f"Read-only command failed: {argv[0]} (exit {result.returncode})")
    return result.stdout


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--checkout", type=Path, required=True)
    p.add_argument("--commit", required=True)
    p.add_argument("--session", required=True)
    p.add_argument("--file", required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--code-ref", required=True)
    p.add_argument("--hosted-repo")
    p.add_argument("--require-uploaded", action="store_true")
    p.add_argument("--task", help="Native child agent ID stored under the parent checkpoint")
    args = p.parse_args()
    root = args.checkout.resolve()
    if args.output.exists():
        raise SystemExit("Receipt exists; preserve it")
    commit = run(["git", "rev-parse", args.commit], root).decode().strip()
    code_ref_oid = run(["git", "rev-parse", args.code_ref], root).decode().strip()
    run(["git", "merge-base", "--is-ancestor", commit, code_ref_oid], root)
    message = run(["git", "show", "-s", "--format=%B", commit], root).decode()
    if "Co-Authored-By: Codex Desktop " not in message or "Codex-Reasoning-Effort: " not in message or "unavailable" in message:
        raise SystemExit("Exact Codex commit provenance missing")
    metadata = json.loads(run(["entire", "checkpoint", "explain", "--commit", commit, "--json"], root))
    sessions = [s for s in metadata["sessions"] if s["session_id"] == args.session]
    if len(sessions) != 1:
        raise SystemExit("Expected unique native session missing from checkpoint")
    session = sessions[0]
    if session.get("agent", "").lower() != "codex" or (not args.task and args.file not in session.get("files_touched", [])):
        raise SystemExit("Expected Codex file event absent from metadata")
    transcript_args = ["entire", "checkpoint", "explain", "--commit", commit, "--transcript",
                       "--session-index", str(session["index"])]
    identity_id = args.session
    if args.task:
        tasks = [t for t in metadata.get("tasks", []) if t.get("agent_id") == args.task]
        if len(tasks) != 1 or not tasks[0].get("transcript_stored") or args.file not in tasks[0].get("files", []):
            raise SystemExit("Native child task/transcript/file metadata missing")
        # The native CLI makes --task and --session-index mutually exclusive.
        transcript_args = ["entire", "checkpoint", "explain", "--commit", commit,
                           "--transcript", "--task", args.task]
        identity_id = args.task
    transcript = run(transcript_args, root)
    identities, events = [], []
    names = {args.file, str(root / args.file)}
    for number, raw in enumerate(transcript.splitlines(), 1):
        try:
            item = json.loads(raw)
        except json.JSONDecodeError:
            continue
        payload = item.get("payload", {})
        if item.get("type") == "session_meta" and payload.get("id") == identity_id:
            identities.append({"session_id": payload["id"], "cwd": payload.get("cwd"),
                               "source": payload.get("source")})
        event = payload.get("item", {})
        if item.get("type") == "event_msg" and payload.get("type") == "item_completed" and isinstance(event, dict):
            changes = event.get("changes", {})
            paths = set(changes) if isinstance(changes, dict) else {c.get("path") for c in changes if isinstance(c, dict)}
            if event.get("type") in ("FileChange", "file_change") and event.get("status") == "completed" and paths & names:
                events.append({"line": number, "item_id": event.get("id"), "file": args.file})
    if not identities or not any(Path(i["cwd"]).resolve() == root for i in identities) or not events:
        raise SystemExit("Stored native session/cwd/completed FileChange evidence missing")
    refrows = run(["git", "for-each-ref", "--format=%(refname) %(objectname)", "refs/entire/checkpoints"], root).decode().splitlines()
    matches = [r.split() for r in refrows if r.split()[0].endswith("/" + metadata["checkpoint_id"])]
    if len(matches) != 1:
        raise SystemExit("Checkpoint ref identity ambiguous")
    ref, oid = matches[0]
    result = {"verified_at": datetime.now(timezone.utc).isoformat(), "checkout": str(root),
              "commit": commit, "code_ref": args.code_ref, "checkpoint_id": metadata["checkpoint_id"],
              "code_ref_oid": code_ref_oid, "child_task_id": args.task,
              "checkpoint_ref": ref, "checkpoint_oid": oid, "branch": metadata.get("branch"),
              "session_id": args.session, "all_checkpoint_session_ids": [s["session_id"] for s in metadata["sessions"]],
              "native_capture_verified": True, "identities": identities, "file_events": events,
              "transcript_sha256": hashlib.sha256(transcript).hexdigest(), "transcript_bytes": len(transcript),
              "private_guidance_marker_hits": [s for s in ("memory/transport.json", "sensitive transport configuration",
                 "private overlay", "Hub token file") if s.encode() in transcript],
              "raw_transcript_saved": False, "uploaded_refs_verified": False, "hosted_verified": False}
    if args.require_uploaded:
        remote = run(["git", "remote", "get-url", "--push", "origin"], root).decode().strip()
        if not remote.startswith("git@github.com:"):
            raise SystemExit("Expected configured SSH push remote")
        refs = {args.code_ref: code_ref_oid, ref: oid}
        actual = dict(reversed(row.split()) for row in run(["git", "ls-remote", "--refs", remote, *refs], root).decode().splitlines())
        if actual != refs:
            raise SystemExit("Uploaded refs differ from expected exact OIDs")
        result["uploaded_refs_verified"] = True
    if args.hosted_repo:
        hosted = json.loads(run(["entire", "checkpoint", "explain", metadata["checkpoint_id"],
                                "--repo", args.hosted_repo, "--json"], root))
        ids = [s["session_id"] for s in hosted.get("sessions", [])]
        result["hosted_verified"] = hosted.get("checkpoint_id") == metadata["checkpoint_id"] and args.session in ids
        result["hosted_session_ids"] = ids
        if args.task:
            result["hosted_child_task_verified"] = any(t.get("agent_id") == args.task and t.get("transcript_stored")
                for t in hosted.get("tasks", []))
            result["hosted_verified"] = result["hosted_verified"] and result["hosted_child_task_verified"]
        if not result["hosted_verified"]:
            raise SystemExit("Hosted metadata did not match")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
