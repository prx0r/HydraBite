# Submission — MemoryProof + WigglyMem

**Track:** 03 — Memory + Context Retrieval
**Prize:** $5,000

---

## 1. The Solution

### 1.1 Overall

MemoryProof + WigglyMem is a two-part system for graph memory:

1. **WigglyMem** — A working memory system built on HydraDB that stores verified scholarly evidence as knowledge sources with graph-enriched recall.

2. **MemoryProof** — A benchmark suite that proves whether graph memory actually works, using Wiggly's verified corpus as ground truth.

Together: **"We built memory AND proved it works."**

**Problem:** Agent memory systems retrieve plausible context. Nobody systematically tests whether it's correct, attributable, or consistent.

**Audience:** Developers building agent memory, researchers needing reproducible context, anyone using HydraDB.

### 1.2 Quick SWOT

| Helpful | Harmful |
|---------|---------|
| **Strengths:** Unique benchmark, real ground truth, HydraDB-native, reproducible | **Weaknesses:** Requires Wiggly corpus setup, limited to scholarly domain |
| **Opportunities:** Could become HydraDB's official benchmark, reusable across memory systems | **Threats:** HydraDB might build their own benchmark |

### 1.3 The Story

**The question:** Does HydraDB's graph memory actually return correct, attributable, consistent context?

**The journey:** We started building a knowledge graph. Then we realized nobody tests whether graph memory works. So we built the test.

**The insight:** Fast mode achieves X% accuracy, thinking mode achieves Y%. The difference matters for production deployments.

**What others can reuse:** Benchmark suite, failure taxonomy, ground truth format, HydraDB evaluation methodology.

---

## 2. Technical

### 2.1 Architecture

```
Wiggly Ground Truth → HydraDB Knowledge Sources
    │
    ├── hydradb_query (fast)
    ├── hydradb_query (thinking)
    └── hydradb_graph_query (Cypher)
    │
    ▼
BenchmarkResults → FailureAnalysis → Auto-tune
```

### 2.2 HydraDB Elements Used

| Tool | What |
|------|------|
| `hydradb_ingest` | Store Wiggly evidence as knowledge sources |
| `hydradb_query` | Test fast vs thinking recall |
| `hydradb_graph_query` | Test Cypher graph traversal |
| `hydradb_list` | Verify export completeness |

### 2.3 Reproducibility

```bash
pip install -e .
memoryproof evaluate --count 50
memoryproof report
```

---

## 3. Links

- Code: https://github.com/prx0r/neverbrokeagain-hackathon2
- Demo: `python demo.py`
