# The one-line architectural patch to HydraDB's AI Chief of Staff recipe

HydraDB's current recipe has the right division of labor: HydraDB selects functions and the application orchestrator executes them. Iolaus does **not** put routing intelligence back in the orchestrator.

It changes the feedback boundary.

## Before

Conceptually:

```python
suggestion = hydra.select_function(task)
result = registry[suggestion.function_id](suggestion.arguments)

# execution outcome becomes future memory / learning signal
hydra.ingest_memory(
    f"Executed {suggestion.function_id}. Result: {summarize(result)}"
)
```

## With Iolaus

```python
suggestion = hydra.select_function(task)
contract = contracts[suggestion.function_id]
tool = registry[suggestion.function_id]
verifier = verifiers[contract.allowed_verifier_ids[0]]

pending = bite.execute(
    contract,
    tool,
    suggestion.arguments,
    executor="chief-of-staff",
)

# At this point tool output is an OBSERVATION, even if it says success=true.
result = bite.verify(contract, pending, verifier)

if result.status == "VERIFIED":
    hydra.ingest_memory(
        f"Verified execution {suggestion.function_id}; "
        f"receipt={result.receipt.receipt_hash}"
    )
else:
    # Route retry / compensation / human escalation using the existing orchestrator.
    handle_unverified(result)
```

The orchestrator remains thin. HydraDB remains the selection/reasoning layer. Iolaus gives the orchestrator a principled distinction between:

```text
CALL RETURNED
and
DECLARED EFFECT VERIFIED
```

## Contract examples

### Calendar booking

```text
requires:
  contact:<alice>:resolved

produces:
  calendar:event:<request-id>:exists

verifier:
  calendar.readback.v1

postcondition:
  returned event ID exists and attendee/start time match request
```

### Deployment

```text
requires:
  build:<sha>:verified

produces:
  deployment:<sha>:healthy

verifier:
  service.healthcheck.v2

postcondition:
  deployed SHA matches + readiness endpoint passes
```

### Coding agent

```text
requires:
  repo:<sha>:checked_out

produces:
  task:<issue>:fixed

verifier:
  test-suite:<revision>

postcondition:
  required regression tests pass on produced revision
```

## Why this improves self-improvement

Self-improving routing is only as good as its outcome labels. If “success” is populated from executor self-report, silent semantic failures become noisy positive examples.

Iolaus changes the outcome signal to:

```text
VERIFIED / REJECTED / BLOCKED / EXECUTION_FAILED
```

and attaches an evidence path. The existing Hydra feedback loop can then learn from a cleaner target without Iolaus becoming another router.
