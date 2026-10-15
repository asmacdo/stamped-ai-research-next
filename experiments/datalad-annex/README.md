# DataLad and annex working example

This synthetic fixture uses SciPy's one-sample t test, a pandas result table, and a Matplotlib figure.
Its five input values are a known-answer integration check, not research observations.
The computation uses the root Pixi environment.

After the source is committed and the checkout provenance hook is prepared, run once from the repository root.
Use a fresh run ID and the prepared hook initializer and exact provenance resolver supplied by the coordinator:

```sh
pixi run --locked duct -p experiments/datalad-annex/logs/toy-001/run_ \
  --fail-time 0 --capture-outputs all --outputs all --record-types all \
  python experiments/datalad-annex/trial.py --run-id toy-001 \
  --initializer scripts/prepare_checkout.py \
  --resolver /Users/johnlee/.agents/skills/commit-provenance/scripts/resolve.sh
```

The trial creates a real DataLad run commit on the current task branch.
Fresh external clones receive the exact ignored lock and their own installed root environment.
They test native discovery failure, explicit compatibility replay, discovery/replay of the replay-created commit, and a zero-exit no-op that the independent verifier must reject.
Another clone retrieves the annexed table from its explicit local origin.
Online delivery is a separate coordinator check.

`receipts/<run-id>/` preserves every subprocess stream, command outcome, environment hashes, hook preparation receipts and individual checks.
Timeouts and spawn failures retain partial or empty streams.
`logs/<run-id>/` is the complete outer duct capture; inspect its final summary after the process exits.
Live verification clones remain at the external temporary path in the receipt; they are not copied into the project or archived as experiment source.

The expected table has n=5, mean=3, df=4 and t²=18.
The verifier uses fixed fixture identities independently of SciPy and checks the rendered figure files.
Review `outputs/figure.png` visually as well.
Retain the successful run's lock bytes and hash for the separate environment snapshot branch; never regenerate that lock later to approximate this run.

On failure, inspect the first receipt.
Fix only the demonstrated issue and use a new run ID for a justified attempt.
Do not silently reuse existing outputs.
The prepared commit hook must resolve exact provenance afresh for every authored commit; unavailable provenance is a coordinator handoff, not permission to guess.
