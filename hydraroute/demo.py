#!/usr/bin/env python3
"""HydraRoute Demo — Agent Toolchain Compiler on HydraDB."""
import json
from hydraroute.hydra import HydraRoute
from hydraroute.schema import DEFAULT_TOOLS
from hydraroute.planner import Planner
from hydraroute.qdw_integration import QDWCapabilityGraph

print("=" * 60)
print("  HydraRoute — Agent Toolchain Compiler")
print("  Hack Hydra Track 03")
print("=" * 60)

# === PART 1: Ingest tools into HydraDB ===
print("\n[1] Ingesting 20 MCP tools into HydraDB...")
hydra = HydraRoute()
graph = QDWCapabilityGraph()

# Simulate ingesting tools
for tool in DEFAULT_TOOLS:
    graph.tools.append({
        "name": tool.name,
        "provider": tool.provider or "local",
        "cost": tool.cost,
        "latency": tool.latency,
        "reliability": tool.reliability,
        "free": tool.cost == 0,
        "context_tokens": 0,
        "tools_supported": True,
    })

print(f"   Ingested {len(graph.tools)} tools")
print(f"   Generated {len(graph.to_hydra_cypher())} Cypher statements")

# === PART 2: Find routes ===
print("\n[2] FIND ROUTE: repo + issue → tested_patch")
print("─" * 50)
planner = Planner(hydra)
routes = planner.plan(
    have=["repo", "issue_number"],
    want="tested_patch",
    tools=DEFAULT_TOOLS,
    max_cost=0.10,
)
for i, r in enumerate(routes[:3]):
    print(f"  Route #{i+1}")
    for step in r.steps:
        print(f"    → {step}")
    print(f"    cost: ${r.cost:.3f} | latency: {r.latency:.1f}s | reliability: {r.reliability:.0%}")
    print()

# === PART 3: Budget constraint ===
print("[3] BUDGET CONSTRAINED: max_cost=$0.01")
print("─" * 50)
routes = planner.plan(have=["repo", "issue_number"], want="tested_patch", tools=DEFAULT_TOOLS, max_cost=0.01)
print(f"   Routes found: {len(routes)}")
if routes:
    for r in routes:
        print(f"   Route: {' → '.join(r.steps)}")
        print(f"   Cost: ${r.cost:.3f}")
print()

# === PART 4: Disable a tool ===
print("[4] DISABLE deepseek.patch (model unavailable)")
print("─" * 50)
routes = planner.plan(
    have=["repo", "issue_number"],
    want="tested_patch",
    tools=DEFAULT_TOOLS,
    max_cost=0.10,
    disabled=["model.patch"],
)
for r in routes:
    print(f"   Route: {' → '.join(r.steps)}")
    print(f"   Cost: ${r.cost:.3f}")
print()

# === PART 5: Different goal ===
print("[5] DIFFERENT GOAL: repo → summary")
print("─" * 50)
routes = planner.plan(have=["repo"], want="summary", tools=DEFAULT_TOOLS)
for r in routes:
    print(f"   Route: {' → '.join(r.steps)}")
    print(f"   Cost: ${r.cost:.3f}")
print()

# === PART 6: Show all tools ===
print("[6] AVAILABLE TOOLS (20)")
print("─" * 50)
for t in DEFAULT_TOOLS:
    print(f"  {t.name:<25} cost: ${t.cost:.3f} | lat: {t.latency:.1f}s | rel: {t.reliability:.0%}")
print()

print("=" * 60)
print("  MCP standardized how agents call tools.")
print("  HydraRoute explores how agents choose paths.")
print("=" * 60)
