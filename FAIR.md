# FAIRness of Pāṭala Research CI

FAIR is treated as an implementation constraint, not a slogan.

## Findable

- Stable public GitHub repository and commit history.
- `CITATION.cff`, `codemeta.json` and `.zenodo.json` included.
- Human-readable IDs for analyses/claims/obligations plus content digests for exact state.
- A DOI-ready Zenodo metadata file is included for archiving a release.

## Accessible

- Core demo runs locally with Python 3.10+ and no required network dependency.
- Source code is MIT licensed; submission documentation is CC BY 4.0.
- OpenAIRE-derived metadata follows OpenAIRE's CC BY terms and attribution.
- No credentials are committed; live services are optional adapters rather than hidden prerequisites.

## Interoperable

- OpenAIRE Graph V3/V4, ScholeXplorer and Broker adapters.
- Official OpenAIRE/Alien MCP is explicitly supported as the agent discovery plane.
- Pāṭala exposes its own MCP tools for continuous verification.
- JSON data models have machine-readable JSON Schemas under `schemas/`.
- Portable exports use the RO-Crate 1.2 layout and JSON-LD metadata.
- PIDs/OpenAIRE IDs are retained instead of replaced by local opaque strings wherever possible.

## Reusable

- Deterministic fixtures and adversarial tests.
- Explicit limitations and source-health semantics.
- Frozen resolution plans and hashable evidence receipts.
- No OpenAIRE-specific logic in the core diff/impact semantics; another scholarly source can implement the same `Snapshot` boundary.
- `PREEXISTING.md` and `docs/REUSE.md` disclose prior work and reused design mechanisms.
