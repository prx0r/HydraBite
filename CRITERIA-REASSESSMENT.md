# Criteria Reassessment

*After reviewing the official hackathon scoring criteria*

---

## The6 criteria

1. **Use of AI MCP connector** that uses the OpenAIRE Graph API
2. **Usefulness and value** — solves a real problem, unlocks a clear use case
3. **Originality** — fresh approach, thoughtful design, unexpected combinations
4. **Responsible use of data** — respects rights, provenance, source policies
5. **Reproducibility and interoperability** — others can re-run, re-apply, re-extend
6. **Clarity** — simple story, clear demo, documented choices

---

## Research CI — still #1 but criterion 1 is a gap

| Criterion | Score | Notes |
|-----------|-------|-------|
| 1. MCP connector | **3/5** | Uses V3 API directly. Need to show MCP integration. |
| 2. Usefulness | **5/5** | Living reviews + AI agents. 318M relations removed in one release. |
| 3. Originality | **5/5** | No existing end-to-end analysis→dependency→impact→obligation tool. |
| 4. Responsible | **5/5** | Append-only, anti-cheat, frozen acceptance, human authority. |
| 5. Reproducibility | **5/5** | Content-addressed, deterministic, 12 attack fixtures, 1 dependency. |
| 6. Clarity | **5/5** | One question, one loop, one demo. |

**Total: 28/30**

### Fix needed: MCP integration

The hackathon specifically says "Use of AI MCP connector that uses the OpenAIRE Graph API." The Alien MCP is the tool they want demonstrated.

Two approaches:
1. **Research CI as an MCP tool** — register our verification as a tool that agents can call through MCP. This is actually MORE interesting than just using MCP as input.
2. **MCP adapter** — add a thin adapter that reads through MCP instead of raw V3.

Option 1 is strategically better: "We don't just consume the MCP — we extend it."

---

## Other ideas — do any score higher?

| Idea | C1 (MCP) | C2 (Useful) | C3 (Original) | C4 (Responsible) | C5 (Repro) | C6 (Clear) | Total |
|------|----------|-------------|---------------|-------------------|------------|------------|-------|
| **Research CI** | 3 | 5 | 5 | 5 | 5 | 5 | **28** |
| Research CI + MCP adapter | **5** | 5 | 5 | 5 | 5 | 5 | **30** |
| Broker Agent | 4 | 4 | 3 | 4 | 4 | 4 | 23 |
| Scholar Relay | 4 | 4 | 4 | 4 | 3 | 4 | 23 |
| Crux | 2 | 4 | 5 | 4 | 4 | 3 | 22 |
| Counterfactual | 2 | 3 | 5 | 4 | 3 | 3 | 20 |
| OpenScience CI | 2 | 3 | 4 | 4 | 5 | 3 | 21 |
| Contribution Ledger | 2 | 4 | 4 | 4 | 3 | 3 | 20 |

**Research CI with MCP integration is still the best.** No other idea scores higher even with the MCP bonus.

### Why not Broker Agent?

Broker Agent naturally uses MCP (it processes Broker events). But:
- Originality is lower (metadata enrichment is common)
- Usefulness is narrower (only repositories)
- The evidence bundle idea is good but the core is "validate OpenAIRE's suggestion"

### Why not Scholar Relay?

Scholar Relay could use MCP to find experts. But:
- Reproducibility is lower (human routing is hard to benchmark)
- The demo would be "find a researcher" — less compelling than "your conclusion is stale"

---

## Conclusion

**Research CI is still #1.** Add MCP integration to score 5/5 on criterion 1.

The MCP integration is actually a natural fit: Research CI becomes an MCP tool that agents can call to check if their conclusions are still valid. That's not just "using the MCP" — it's extending the MCP with verification capabilities.
