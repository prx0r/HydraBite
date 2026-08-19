# Hack Hydra final submission checklist

Based on the public Hack Hydra event page reviewed 2026-08-19. The release agent should re-open the live page immediately before submission in case instructions changed.

## Event fit

- [x] Built specifically with the **HydraDB open-source repository/runtime**, not only hosted Hydra services.
- [x] Focused scope with technical depth rather than a thin generic demo.
- [x] Originality is in a Hydra-native execution trust boundary, not another memory/RAG wrapper.
- [x] Concrete working demo with real external side effect/readback semantics.
- [x] Clear downstream capabilities unlocked without pretending they are already implemented.

## Evidence required before public submission

- [ ] `validation/RUN_CERTIFICATE.json` says `PROVEN_LIVE_HYDRADB`.
- [ ] Certificate generated from the final commit, not an earlier build.
- [ ] Hydra runtime image RepoDigest recorded.
- [ ] `algo.MSpaths` live probe is true.
- [ ] Integration suite passes on the exact release code.
- [ ] False-success benchmark is generated, not manually edited.
- [ ] Demo video shows both FAIL and PASS paths.
- [ ] README contains real video/repository links.
- [ ] Presentation exported and opens correctly.
- [ ] Research identifiers rechecked; no uncertain citation presented as exact.
- [ ] Old MemoryProof/OpenAIRE/Hackathon1 files removed from judge-facing root.

## Submission story in one sentence

**HydraDB already helps agents decide what action to take; Iolaus makes execution outcomes earn a verifier receipt before they can become trusted graph state or future learning signal.**
