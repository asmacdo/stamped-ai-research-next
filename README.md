# STAMPED research with agents

A prepared repository for comparing research agents with and without STAMPED guidance.
[prompt.md](prompt.md) defines the study; [AGENTS.md](AGENTS.md) defines the project conventions.

Add experiments under `experiments/` and dependencies to the root `pixi.toml`.
Concurrent agents use prepared external worktrees with installed submodules.
Git stores source and metadata; git-annex stores larger artifacts and execution records on [CON Hub](https://hub.centerforopenneuroscience.org/leej3/stamped-ai-research-next).

Run `pixi task list` for available commands.
`pixi run launch --help` describes worker launches; [host configuration](scripts/README.md) supplies the existing machine-specific paths.
Working locks stay ignored; preserve the exact validated lock on a separate snapshot commit above the final task commit.

The core STAMPED workflows are tool-neutral.
Project-specific environment guidance belongs in `pixi-with-stamped`.
Pin assessment separately from the workflows being improved.

Execution trials and their complete records are retained under `experiments/`.
They establish the tested execution routes, not scientific or skill efficacy.
