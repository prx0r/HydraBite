# Challenge: Adaptive Knowledge Graph

## The hard truth

**DeepTutor already exists.** It implements graph-enhanced RAG tutoring with Neo4j. pykt-toolkit has 429 stars and is the standard benchmark for knowledge tracing. The educational KG-RAG space is heating up fast.

Your `adaptive-knowledge-graph` repo is a solid prototype but it's **not particularly novel** compared to what's already out there.

## What's actually different

The only genuinely different angle: using a **real scholarly knowledge graph** (OpenAIRE) as the knowledge source instead of textbook ontologies. Most educational AI uses flat concept prerequisite graphs. OpenAIRE gives you publications, datasets, software, researchers, and their connections.

But that's a thin differentiation. A judge would ask: "Why not just use OpenAlex directly?"

## Competitors

| Repo | Stars | What it does | Threat |
|------|-------|-------------|--------|
| [DeepTutor](https://github.com/ndpvt-web/deeptutor-claude-skill) | 27 | Graph-enhanced RAG tutoring | HIGH — direct competitor |
| [pykt-toolkit](https://github.com/pykt-team/pykt-toolkit) | 429 | Knowledge tracing benchmark | HIGH — standard evaluation |
| [adaptive-knowledge-graph](https://github.com/MysterionRise/adaptive-knowledge-graph) | 15 | Your own prototype | REFERENCE |
| [cs-course-knowledge-graph](https://github.com/tian1220A/cs-course-knowledge-graph) | 1 | CS course KG | LOW |
| OpenAlex | — | 240M+ works, free API | DATA SOURCE — not competitor |

## Reusable from competitors

- pykt-toolkit's evaluation metrics (AUC, RMSE, etc.)
- DeepTutor's graph-RAG architecture
- Bayesian Knowledge Tracing as baseline
- OpenAlex as data source (free, larger than OpenAIRE for this use case)

## Verdict

**Already built, already competed.** The repo exists, the space is crowded, the differentiation is thin. Not worth pursuing for this hackathon unless you have a genuinely novel educational angle that goes beyond "OpenAIRE as textbook."

Don't submit this. Reference it as "existing work" if needed.
