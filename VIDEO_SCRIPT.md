# Video walkthrough script (target: ~2 minutes)

## 0:00–0:15 — Problem

“OpenAIRE continuously improves its scholarly graph. That is good — but an AI agent may have stored a conclusion from last month's graph. When the graph changes, which conclusions actually need checking again?”

## 0:15–0:35 — MCP use

Show an AI client with the official OpenAIRE MCP / Open Science plugin.

“First, the agent discovers evidence through the OpenAIRE MCP powered by Alien Intelligence. Pāṭala records the exact tool call and OpenAIRE identifiers as a credential-redacted, hashed trace.”

Show `patala-ci mcp-import ...` or the Pāṭala MCP `record_openaire_mcp_call` tool.

## 0:35–0:55 — Track

Run the deterministic demo or show:

```bash
patala-ci track ... --api v3 --claims claims.json --mcp-trace alien-trace.json
```

“Pāṭala then creates a deterministic Graph V3 snapshot and records explicit dependencies between evidence and conclusions.”

## 0:55–1:20 — Change and impact

Run:

```bash
patala-ci verify <analysis-id>
```

“Here one record was added and one dataset relation disappeared. The important result is not the diff: two claims need recomputation, while unrelated claims remain untouched.”

## 1:20–1:40 — Proof obligation

Show a `ProofObligation` and `ResolutionPlan`.

“An affected claim gets a frozen proof obligation. It cannot silently return to current because an agent says ‘done’; the resolution produces a verifiable evidence receipt.”

## 1:40–2:00 — Why OpenAIRE

“OpenAIRE continuously validates research information. Pāṭala continuously validates what researchers and agents derived from that information. The artifact is MIT/CC-BY, reproducible offline, exports RO-Crate, and can be reused with other evolving scholarly sources.”
