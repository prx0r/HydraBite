# Challenge: OpenScience CI

## The hard truth

**This is almost entirely unoccupied.** There's no adversarial testing framework for scholarly knowledge graphs. That's both exciting (blue ocean) and concerning (maybe nobody wants it).

The closest analogue is property-based testing in software (Hypothesis, QuickCheck). But translating that to scholarly graphs requires defining invariants that are meaningful — and "same surname + different country should not merge" is a toy example.

## The real question

Who runs these tests? OpenAIRE themselves? Repository managers? Researchers?

If OpenAIRE: they already do internal validation. You'd be building a tool for a team that already has one.
If repository managers: they don't have the expertise.
If researchers: they don't care about graph invariants.

The strongest customer is probably **research infrastructure evaluators** — people who need to assess whether a scholarly graph is trustworthy before building on it. That's a niche within a niche.

## Competitors

| Repo | Stars | What it does | Threat |
|------|-------|-------------|--------|
| None found | — | No adversarial testing for scholarly KGs | **WIDE OPEN** |
| LUBM/AMIE+ benchmarks | — | Generic KG benchmarks | ADJACENT — not scholarly |
| Hypothesis (Python) | — | Property-based testing framework | REFERENCE — pattern to follow |
| OpenAIRE contract tests | — | API-level regression testing | ADJACENT — different layer |

## Reusable from competitors

- Hypothesis's property-based testing patterns
- LUBM's benchmark methodology
- OpenAIRE's contract test architecture as reference
- QDW's verification framework from existing repos

## Verdict

**Best dev tool but hard to demo.** The "CI for scholarly graph integrity" framing is novel. But the customer is unclear and the demo is dry (test suites pass/fail). Better as a **component of Research CI** — "Research CI includes invariant checking" — than a standalone submission.

Position as: "Built-in quality layer. Research CI runs adversarial invariants before trusting graph state."
