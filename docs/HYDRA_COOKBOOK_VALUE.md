# Value to HydraDB's current action recipes

## The exact seam

HydraDB's AI Chief of Staff recipe describes a clean separation:

```text
User / Agent
     ↓
Action Orchestrator
     ↓
HydraDB function selection
     ↓
Policy / auth
     ↓
External API execution
     ↓
Execution result
     ↓
HydraDB feedback / memory
```

The recipe's strength is intelligent function routing and composition. Iolaus inserts only one thing between `Execution result` and `feedback`:

```text
External API
     ↓
HBObservation: SUCCEEDED_UNVERIFIED
     ↓
contract-authorized verifier
     ↓
┌───────────────┬─────────────────┐
│ FAIL          │ PASS            │
│               │                 │
│ rejected      │ Bite receipt    │
│ no claim      │ verified claim  │
└───────────────┴─────────────────┘
                    ↓
             safe feedback signal
```

## Why it matters to the cookbook's examples

### Customer success
Current sequence can create a demo meeting, update CRM and send confirmation.
Iolaus prevents `send_confirmation_email` from being enabled by a calendar API that merely *reported* a booking. A calendar readback can certify the meeting ID/start time first.

### Executive assistant
“Prepare the board meeting” spans generated documents, calendar state, reminders and KPI sources. Each irreversible action can declare a different verifier strength instead of treating all `success` responses equally.

### DevOps incident response
`scale_database_resources` returning success is weaker than `service_health == healthy` after the scale operation. Iolaus turns health/readiness into the postcondition that enables the status update or closes remediation.

### Finance / approvals
The recipe already calls out policy and approval workflows. Iolaus complements them: authorization answers **may this action run?**; verification answers **did the authorized action actually achieve its declared effect?**

## The benchmark gap Iolaus adds

The full Function Routing cookbook reports a useful evaluation surface around thousands of tasks, dozens of registered functions, routing accuracy, multi-step completion, personalization, suggestion acceptance, and latency.

Iolaus does not compete with those numbers. It adds a missing orthogonal axis:

```text
FALSE-SUCCESS COMMIT RATE
= promoted trusted transitions
  where the declared postcondition was actually false
  / semantic failures
```

A second metric follows naturally:

```text
VERIFIED COMPLETION RATE
= transitions with a valid PASS receipt
  / attempted transitions
```

This improves the quality of the very execution history HydraDB uses for self-improving function selection.

## Why a graph is useful here

The value is not merely storing receipts. A graph preserves the causal/audit path:

```text
claim
← receipt
← invocation
← contract
← prerequisites
```

This means a future Hydra agent can ask:
- What exact evidence authorized this downstream action?
- Which verifier certified the prerequisite?
- Which workflows historically reach a verified terminal state?
- Which tool's optimistic success most often becomes a FAIL receipt?

HydraDB already has native bounded path procedures, so these become graph queries rather than reconstructed log joins.
