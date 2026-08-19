"""QDW → HydraDB capability graph integration.

This module exports QDW's HotSwap routing infrastructure into HydraDB
as a capability graph, then uses HydraDB's path procedures for
visualization and constrained planning.
"""
import json
from typing import Any

# QDW types (from qdw/hotswap/types.py)
# Route, TaskSpec, CandidateAssessment, ExecutionPlan

class QDWCapabilityGraph:
    """Export QDW routing state to HydraDB capability graph."""

    def __init__(self):
        self.tools = []
        self.capabilities = []
        self.edges = []

    def from_qdw_routes(self, routes: list[dict]) -> None:
        """Convert QDW Route objects to capability graph."""
        for route in routes:
            # Tool node
            self.tools.append({
                "name": route.get("model_id", "unknown"),
                "provider": route.get("provider_id", "unknown"),
                "cost": route.get("fixed_request_cost_usd", 0) or
                        (route.get("input_per_m", 0) + route.get("output_per_m", 0)) * 1000 / 1_000_000,
                "latency": route.get("latency_ms", 1000) / 1000,
                "reliability": route.get("reliability", 0.95),
                "free": route.get("free", False),
                "context_tokens": route.get("context_tokens", 0),
                "tools_supported": route.get("tools_supported", False),
            })

    def from_dell_providers(self, providers: list[dict]) -> None:
        """Convert Dell provider data to capability graph."""
        for prov in providers:
            self.tools.append({
                "name": prov.get("name", "unknown"),
                "provider": prov.get("provider_id", "unknown"),
                "cost": prov.get("cost_per_1k", 0) * 1000 / 1_000_000,
                "latency": prov.get("latency_p50_ms", 1000) / 1000,
                "reliability": prov.get("success_rate", 0.95),
                "free": prov.get("free_tier", False),
                "context_tokens": prov.get("context_window", 0),
                "tools_supported": prov.get("function_calling", False),
            })

    def to_hydra_cypher(self) -> list[str]:
        """Generate Cypher statements for HydraDB ingestion."""
        statements = []
        for tool in self.tools:
            statements.append(f"""
            MERGE (t:Tool {{name: '{tool["name"]}'}})
            SET t.provider = '{tool["provider"]}',
                t.cost = {tool["cost"]},
                t.latency = {tool["latency"]},
                t.reliability = {tool["reliability"]},
                t.free = {tool["free"]},
                t.context_tokens = {tool["context_tokens"]}
            """)
        return statements

    def find_routes(self, have: list[str], want: str) -> list[dict]:
        """Find routes using QDW's Pareto-frontier logic."""
        routes = []
        for tool in self.tools:
            if want in self._produces(tool):
                reqs = self._requires(tool)
                if all(r in have for r in reqs):
                    routes.append({
                        "tool": tool["name"],
                        "cost": tool["cost"],
                        "latency": tool["latency"],
                        "reliability": tool["reliability"],
                    })
        routes.sort(key=lambda r: (r["cost"], -r["reliability"]))
        return routes

    def _produces(self, tool: dict) -> list[str]:
        """What capabilities this tool produces."""
        name = tool["name"]
        if "patch" in name: return ["patch", "code_change"]
        if "test" in name: return ["test_result", "verified_patch"]
        if "pr" in name: return ["pull_request"]
        if "issue" in name: return ["issue_text"]
        if "search" in name: return ["search_results", "source_context"]
        if "summarize" in name: return ["summary"]
        if "classify" in name: return ["classification"]
        return []

    def _requires(self, tool: dict) -> list[str]:
        """What capabilities this tool requires."""
        name = tool["name"]
        if "patch" in name: return ["source_context", "issue_text"]
        if "test" in name: return ["patch", "repo"]
        if "pr" in name: return ["repo", "patch", "title"]
        if "issue" in name: return ["repo", "issue_number"]
        if "search" in name: return ["repo", "query"]
        return []
