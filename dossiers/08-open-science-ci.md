# Dossier 8: OpenScience CI

**Status:** Best dev tool, strong but ambitious
**Score:** 6.5/10
**Category:** Property-based and adversarial testing for scholarly graphs

---

## TL;DR

Generate adversarial test cases for scholarly graph invariants. Same surname + different country should not merge. DOI in Crossref but different DOI in repository should flag. Publication predating its grant should fail.

---

## The Problem

OpenAIRE spends serious engineering effort avoiding false relationships. IIS tightened affiliation matching and tested against millions of relations. But there's no systematic adversarial testing framework for scholarly graphs.

---

## The Product

```bash
scholar-ci test openaire

# Runs invariant suite:
# ✓ same surname + different country → not merged
# ✓ same org alias + different ROR → not merged
# ✗ DOI in Crossref ≠ DOI in repository → FLAGGED
# ✓ dataset relation + cited DOI resolves → OK
# ✗ grant relation + publication predates project → FLAGGED
# ✓ author ORCID + consistent affiliation → OK

scholar-ci adversarial

# Generates new test cases:
# "Author with 2 DOIs in different repositories"
# "Paper with dataset link but dataset was retracted"
# "Funding relation to expired grant"

scholar-ci replay baseline.json

# Re-runs previous test suite to detect regressions
```

---

## Reusable

- QDW verification framework from qdw/qdw/proof/
- OpenAIRE contract tests pattern from github.com/openaire/openaire-api-contract-tests
- Invariant definitions from fuck-off/lib (epistemic.py, review.py)

## New code needed (~300 lines)

Invariant definitions + adversarial case generator + test runner.

---

## Why this is eighth

Genuinely useful for research infrastructure. The OpenAIRE contract-test repo gives a native starting point. But it's more of a dev tool than a hackathon showpiece — harder to demo dramatically.
