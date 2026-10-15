# Native DataLad replay

DataLad run commits keep their native `[DATALAD RUNCMD]` subject and record.
The commit hook appends fresh Codex provenance without placing a Conventional Commit subject before the marker.
Ordinary authored commits stay Conventional.

The trial reuses the SciPy/pandas/Matplotlib fixture, checks closed-form known answers, and performs two generations of native rerun in independent clones.
Each replay starts without generated outputs.
Native report mode must identify the record; complete output hashes and environment hashes must match.

Run with a new evidence ID, from a checkout without this module's outputs:

```sh
pixi run duct -p experiments/datalad-native/logs/native-001/run_ --fail-time 0 \
  python experiments/datalad-native/trial.py --run-id native-001
```

Verified in [native-001](receipts/native-001/summary.json): 15 checks passed, including two native rerun generations with identical TSV, SVG and PNG bytes.
Complete command streams and resource records are retained in [logs/native-001](logs/native-001/).

The provenance resolver comes from the host launch configuration or `--resolver`.
The earlier compatibility experiment remains historical evidence; new native records need no parser adapter.
