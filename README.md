# STAMPED research with agents

Prepared workspace for a second exploratory comparison of research with and without STAMPED skills.
Experiments add ordinary files under `experiments/` and dependencies to the root `pixi.toml`.
Concurrent agents use separate Git worktrees; their changes merge into this project.
Inputs and reusable skills can be installed submodules.
Large artifacts and execution records use git-annex.

`skills/` starts from [con/skills PR #23](https://github.com/con/skills/pull/23), commit `15da761f63a5a45c507e6596a549720bd43a1e84`.
Local adaptations use `codex/pr23-stamped-rerun`; Austin's source branch is not modified.
The original pilot remains at [stamped-ai-research](https://github.com/leej3/stamped-ai-research).

The research run starts from `prompt.md` after the preparation trials pass.
