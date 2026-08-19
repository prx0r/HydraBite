#!/usr/bin/env bash
set -euo pipefail
WORKSPACE="${1:-.patala-live}"
python -m patala_research_ci.cli --workspace "$WORKSPACE" track \
  --id agentic-ai-software \
  --title "Agentic AI research software" \
  --entity research-products \
  --search "agentic AI" \
  --param type=software \
  --api v3 \
  --page-size 25 \
  --claims examples/live_claims.json
