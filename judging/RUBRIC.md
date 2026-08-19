# Hack Hydra rubric mapping

## Technical depth
- direct HydraDB OSS graph-node HTTP/OpenCypher integration;
- explicit graph invariant separating observation from trusted claim;
- deterministic postcondition verifier path;
- content-bound Ed25519 receipt;
- Hydra-specific native path integration proof;
- failure-oriented live tests rather than happy-path screenshots.

## Originality
Not another memory store or generic tool router. HydraBite focuses on the **execution commit boundary**: when real-world agent actions may safely become shared graph state and future learning signal.

## Execution quality
One command (`scripts/certify.sh`) runs the actual Hydra container, real graph proof, integration suite, adversarial benchmark, demo and evidence certificate. No live test is skipped when Hydra is absent.

## What it enables
Verified-transition history makes downstream routing, self-healing plans, cost-per-verified-success, reputation, approval chains and external validation protocols much safer without requiring those systems in the MVP.
