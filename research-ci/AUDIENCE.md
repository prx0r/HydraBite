# Audience

## Primary: researchers maintaining analyses whose inputs evolve

- Living evidence syntheses
- Systematic/scoping reviews
- Bibliometric/scientometric analyses
- Research-intelligence dashboards
- Policy evidence teams

A real living review documented 30 search updates but only 3 review updates. The expensive question is not "did PubMed/OpenAIRE gain another paper?" but "does this paper change our conclusion?"

## Secondary: AI research agents with persistent research memory

An autonomous research agent may maintain thousands of derived claims. When OpenAIRE changes, rerunning everything is wasteful. Research CI provides incremental invalidation:

```
1000 stored claims
→ 943 unaffected
→ 42 cheap automatic recomputes
→ 12 need deeper evidence retrieval
→ 3 require human judgment
```

## Who does NOT care

- A normal researcher writing one paper
- Anyone building a dashboard (MONITOR exists)
- Anyone building a new graph (OpenAIRE exists)

## The customer test

If you can't answer these, the product fails:

1. Can you distinguish "input changed" from "conclusion changed"?
2. Can you calculate impact rather than just alert?
3. Can you avoid alert fatigue?
4. Can you prove this saves work?
