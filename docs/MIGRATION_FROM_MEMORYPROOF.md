# Migration from the existing Hackathon2 / MemoryProof repository

This pack is designed to replace the judge-facing product direction without requiring the integration agent to salvage the older memory benchmark story.

## Preserve first

Create a branch/tag before deleting anything:

```bash
git checkout -b archive-memoryproof
# push/tag if desired
```

Then create the final HydraBite branch from the desired base.

## Replace judge-facing root

Old material previously observed in the hackathon repository included MemoryProof/WigglyMem messaging plus inherited OpenAIRE Research CI artifacts. Do not leave those alongside HydraBite; it makes the submission look like multiple unrelated products.

Judge-facing canonical files should become:

```text
README.md
SUBMISSION.md
AGENT_INTEGRATION_PROMPT.md
judging/
docs/
research/
presentation/
src/hydrabite/
demo/
benchmarks/
tests/
scripts/
.github/workflows/ci.yml
```

Archive historical experiments under `legacy/` only if retaining them has real value. Do not let their package metadata, console commands, certificates or submission copy remain authoritative.

## P0 deletions / replacements

- Replace old `pyproject.toml` project name/entry point with HydraBite.
- Replace demo importing obsolete packages.
- Remove hosted Hydra MCP as the core backend; HydraBite uses OSS graph-node HTTP.
- Replace stale build certificate with generated live HydraBite certificate only after certification.
- Replace OpenAIRE story/submission/video copy.
- Replace inherited Research CI tests as the main proof surface.

## Keep only if useful as provenance

Older verification concepts can be acknowledged as design lineage, but the final build should remain a standalone small product whose behavior is clear from the root README in under a minute.
