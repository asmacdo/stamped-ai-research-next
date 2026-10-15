# Working rules

- Add experiment files under `experiments/<name>/`; merge useful changes into the project.
  Worktree checkout paths are host infrastructure, not archived experiment directories.
- Use the root Pixi environment.
  Add missing dependencies with `pixi add`; prefer established scientific libraries and tools over custom implementations.
- Keep `pixi.lock` out of task history.
  Preserve the exact final validated lock on `codex/env-<task>-<run>` with one extra commit off the final task commit; publish the snapshot without merging it into main.
- Give concurrent writers separate prepared worktrees and installed submodules.
  Read selected skills from this checkout, not mutable external copies.
- Duct logging is requested for substantive runs in this study.
  Keep complete command, stream, resource and summary records beside the experiment outputs; retain failures.
  Use annex for large artifacts; verify payload retrieval.
  MechaBABS keeps its native records.
- Keep Workshop controls inactive.
  Credentials stay in host providers.
  Ordinary research logs are intended output; never publish credentials or restricted human data.
  Existing pilot captures remain under their prior publication hold.
- Use Conventional Commits and freshly resolved commit-provenance trailers.
  Run Snapper on prose; preserve DataLad and native capture records.
- Adapt reusable skills when a recurring tool problem is demonstrated.
  Keep skill entrypoints concise, route substantial conditional detail to references, and verify behavior after compression.

Scientific trials use the prepared capture and delivery setup.
Check its receipts before launching agents; repair a concrete failure without rebuilding the project.
