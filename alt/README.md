# Alternative implementations

From [neverbrokeagain-research-ci](https://github.com/prx0r/neverbrokeagain-research-ci) — leaner versions of core modules.

These are **not** the submission code. They exist as reference for:
- Simpler diff implementation (works on raw record lists)
- `rich` CLI with pretty tables
- Pydantic-compatible normalization
- Fewer abstractions

## Files

| File | What | Lines |
|------|------|-------|
| `openaire_lean.py` | Leaner V3 client | ~50 |
| `normalize_lean.py` | Focused field extraction | ~30 |
| `diff_lean.py` | Simpler semantic diff | ~50 |
| `cli_rich.py` | Rich CLI with tables | ~100 |

## Why not use these directly

Missing from the submission:
- Anti-cheat invariants (SOURCE FAILURE ≠ ZERO RESULTS)
- Verification module (plans, receipts, attacks)
- Frozen acceptance criteria
- MCP tool definitions
- Attack catalog
- Source status tracking

Use hackathon1/ as the submission. Reference these for style.
