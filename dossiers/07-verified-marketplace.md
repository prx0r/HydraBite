# Dossier 7: Verified-Statement Marketplace

**Status:** Vision E1 from fuck-off, long-term economic flywheel
**Score:** 6.8/10
**Category:** Certification Weight as transferable, compounding trust asset

---

## TL;DR

Verified statements carry Certification Weight — a compounding metric (certification × consensus × load × time) that makes verification a tradeable economic asset. As AI floods the world with content, the scarce resource is trustworthy verified information.

---

## The Problem

AI generates infinite content. Trust is the bottleneck. Nobody currently has a mechanism for:
- Quantifying how verified a statement is
- Making that verification transferable
- Allowing verification to compound over time and use

---

## The Product

```python
CertificationWeight = (
    certification_depth     # how many independent verifiers
    × consensus_score       # agreement among verifiers
    × load_bearing          # how many downstream claims depend on this
    × time_decay            # recent verifications weighted higher
)

# A statement verified by 3 independent sources,
# with high consensus, on which 15 downstream claims depend,
# verified recently
# → HIGH Certification Weight

# A statement verified once, contested, with no downstream dependents,
# verified years ago
# → LOW Certification Weight
```

### Flywheel

```
more verification → higher trust
    → more claims seek certification
        → more downstream builds
            → certification value rises
                → more verification
```

---

## Reusable

- Certificate kernel from fuck-off/lib/certificate.py
- Review reducer from fuck-off/lib/review.py
- Blast-radius from fuck-off/lib/staleness.py

## New code needed (~150 lines)

Marketplace API + pricing model + transfer protocol.

---

## Why this is seventh

Brilliant long-term vision. The flywheel is real. But building a marketplace in a hackathon is ambitious and the economic model needs real testing. Better as a "future vision" slide.
