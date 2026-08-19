# Dossier 10: Adaptive Knowledge Graph

**Status:** Reference architecture from adaptive-knowledge-graph repo
**Score:** 6.0/10
**Category:** Education KG-RAG with Neo4j + OpenSearch + Ollama

---

## TL;DR

A complete educational knowledge graph RAG system: Neo4j concept graph with prerequisite edges, OpenSearch hybrid retrieval (BM25 + vector), local LLM via Ollama, adaptive quizzes with synthetic mastery state, 50+ golden evaluation cases.

---

## The Problem

Educational AI needs:
- Structured knowledge (not just vector search)
- Prerequisite-aware retrieval
- Adaptive practice based on mastery
- Citation grounding

No existing system combines all four in a local-first, evaluable package.

---

## The Product (from existing repo)

```
Next.js UI → FastAPI API → Neo4j KG + OpenSearch + Ollama

Features:
- KG-aware RAG with citations and source snippets
- Concept/module/chunk schema with prerequisite edges
- Hybrid BM25 + vector retrieval
- LLM-generated quizzes with mastery tracking
- 50+ golden evaluation cases
```

---

## Reusable (ALREADY BUILT)

The entire repo at `/root/patalacheckpoints/source-evidence/repos/MysterionRise__adaptive-knowledge-graph/` is a working prototype.

## New code needed

Minimal — it's already a working demo. Would need OpenAIRE data integration.

---

## Why this is tenth

It's already built and works. But it's not particularly novel — educational KG-RAG is an active space. The OpenAIRE hackathon angle would be "OpenAIRE publications as the knowledge source" but that's a stretch. Better as a reference architecture than a submission.
