# Pāṭala Research CI — Thesis

**Continuous trust for OpenAIRE-powered research intelligence**

> When upstream research information changes, identify exactly which downstream analyses, indicators, agent memories, and claims need to be reconsidered.

---

## The one-sentence description

> Pāṭala Research CI tracks the OpenAIRE evidence behind research conclusions and identifies exactly which conclusions require re-verification when that evidence changes.

## Short tagline

> When the evidence changes, know what to recheck.

---

## What it is

A dependency-aware verification layer that:
1. Tracks which research intelligence was used to support a conclusion
2. Detects material upstream changes
3. Determines downstream impact
4. Emits auditable proof obligations for agents or humans to resolve

## What it is NOT

- NOT a graph-diff tool
- NOT a replacement for OpenAIRE's infrastructure
- NOT an AI peer reviewer
- NOT a dashboard

## Architecture

```
TRACK → SNAPSHOT → DETECT → IMPACT → OBLIGE → RESOLVE
```

## Core promise

> OpenAIRE tells you what the research graph knows. Pāṭala remembers what your conclusions depended on — and tells you when they need to be checked again.

## Why OpenAIRE

- 386.6M+ research products
- V3 Graph API (stable, recommended)
- ScholeXplorer V3 (typed relationships)
- Six-month DOI-pinned datasets for reproducibility
- Monthly API state for current intelligence
- Broker for change notifications
- Explicit commitment to continuous validation
- AI agent integration via Alien/MCP
- Theme B (Build) hackathon: working, reusable extension

## Why it matters

OpenAIRE's Aug 2026 release (v11.3.0):
- Added ~6.43M research products
- Removed 318.7M redundant relations
- Removed ~1.05M invalid/duplicate funding relations

A bibliometric analysis depending on a funding relation that disappeared is now wrong. Nobody told the researcher.

Pāṭala does.
