# Workflow pressure scenarios

These cases are the behavioral contract for the seven v2 Skills. They are written before any v2 Skill implementation.

## RED baseline boundary

The v1 repository has five independent documentation-oriented Skills and no Plugin package, orchestrator, digest implementation, risk matrix, controlled commit execution, Draft PR publication, or independent PR validation. The deterministic repository contract must therefore fail before v2 files are created.

Fresh-context model runs are intentionally distinct from static RED/GREEN tests. This session does not claim a behavioral baseline run because the active execution policy does not authorize subagent dispatch. Release readiness requires running every case in `workflow-pressure-cases.yaml` first without the relevant Skill and then with it, recording raw outputs without author reasoning or expected-answer leakage.

### Observed deterministic RED — 2026-08-15

Command: `python -m unittest discover -s tests -p "test_*.py" -v`

- Result: 11 tests; 2 passed, 1 failed, 8 errored.
- Expected missing package errors: repo marketplace, nested Plugin manifest, v2 Skill folders, templates, notice, and CI workflow.
- Expected legacy failure: all five v1 Skill files still existed.
- The two passing checks proved the pressure-scenario inventory and placeholder/link test were runnable before implementation.

This is the required deterministic RED evidence. It is not presented as a substitute for the later fresh-context behavioral release gate.

## Fast contract command

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

The fast suite checks package shape and the explicit rules that close known workflow loopholes. It does not prove probabilistic model compliance.
