# Official OpenAIRE MCP + Pāṭala Research CI

The hackathon explicitly centres the **OpenAIRE MCP plugged into Alien's AI Gateway**. Pāṭala therefore treats that connector as a first-class external dependency, not as something to replace.

## Dual-MCP workflow

```text
AI client
   │
   ├── OpenAIRE MCP (Alien) ──> OpenAIRE Graph
   │       discovery / literature / citation / entity traversal
   │
   └── Pāṭala MCP
           record_openaire_mcp_call
           bind_mcp_trace
           verify_analysis
           list_proof_obligations
```

The official connector supplies agentic discovery. Pāṭala supplies **continuity after the result is stored**.

## Capture a real hackathon evidence trace

1. In the Alien OpenAIRE demo/plugin, run one concrete research query that will seed your demo analysis.
2. Preserve the MCP tool name, non-secret arguments, structured result and explicit OpenAIRE IDs returned by the connector. Do **not** export authentication headers/tokens/cookies.
3. Put them into the trace schema in `schemas/mcp-trace.schema.json`, with:
   - `provider: "Alien Intelligence"`
   - `connector: "OpenAIRE MCP"`
   - `synthetic: false`
4. Import and bind it:

```bash
patala-ci --workspace .patala-live mcp-import artifacts/alien_mcp_trace.live.json \
  --bind <analysis-id>
```

5. Run `patala-ci --workspace .patala-live mcp-list` and `verify-ledger`.
6. Commit **only the credential-redacted trace** if the returned metadata is safe/public under OpenAIRE's terms.

The committed trace gives technical evaluators concrete criterion-1 evidence while Graph V3 remains the replayable state used for deterministic verification.

## Programmatic capture

If the AI client can call both MCP servers, call Pāṭala's `record_openaire_mcp_call` immediately after a successful OpenAIRE MCP call. It accepts the tool name, JSON arguments/result and optional OpenAIRE IDs, sanitizes common credential keys and stores a content digest.

## Offline fixture

`artifacts/alien_mcp_trace.example.json` is **synthetic** and exists only to prove that trace validation, secret redaction, hashing, storage and analysis binding are deterministic. It must never be described as evidence that a credentialed Alien call occurred.

## Why keep V3 as well as MCP?

MCP optimizes AI interaction. Research CI additionally needs a stable machine-replay boundary. OpenAIRE currently documents Graph API V3 as the recommended API, while V4 remains beta. The design therefore records the agent's MCP evidence and binds it to a canonical V3 snapshot. This separation makes the AI interaction inspectable without making long-term reproducibility dependent on an opaque chat transcript.
