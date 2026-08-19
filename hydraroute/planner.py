"""Constrained path planner for agent toolchains."""
from typing import Any
from .schema import ToolDef, Route

class Planner:
    def __init__(self, hydra=None):
        pass

    def plan(self, have: list[str], want: str, tools: list[ToolDef],
             max_cost: float = float("inf"), max_latency: float = float("inf"),
             min_reliability: float = 0.0, disabled: list[str] = None) -> list[Route]:
        disabled = disabled or []

        # Build tool index: capability → tools that produce it
        prod_map = {}
        for t in tools:
            if t.name in disabled:
                continue
            for cap in t.produces:
                prod_map.setdefault(cap, []).append(t)

        # BFS: each state is (have_set, path, cost, latency, reliability)
        routes = []
        start = (frozenset(have), [], 0.0, 0.0, 1.0)
        queue = [start]
        visited = set()

        while queue:
            current_have, path, cost, latency, rel = queue.pop(0)

            state_key = (current_have, tuple(path))
            if state_key in visited:
                continue
            visited.add(state_key)

            # Check if we reached the goal
            if want in current_have and path:
                routes.append(Route(
                    route_id=len(routes)+1, steps=list(path),
                    cost=cost, latency=latency, reliability=rel))
                continue

            # Try each tool that produces something we don't have
            for tool in tools:
                if tool.name in disabled:
                    continue
                if tool.name in path:
                    continue  # avoid cycles

                # Check if this tool produces something new
                new_caps = [c for c in tool.produces if c not in current_have]
                if not new_caps:
                    continue

                # Check if we can afford it
                if tool.cost + cost > max_cost:
                    continue
                if tool.latency + latency > max_latency:
                    continue
                if tool.reliability * rel < min_reliability:
                    continue

                # Check if ALL requirements are met
                if all(req in current_have for req in tool.requires):
                    new_have = current_have | frozenset(tool.produces)
                    queue.append((new_have, path + [tool.name],
                        cost + tool.cost, latency + tool.latency,
                        tool.reliability * rel))

        # Deduplicate and sort
        seen = set()
        unique = []
        for r in routes:
            key = tuple(r.steps)
            if key not in seen:
                seen.add(key)
                unique.append(r)
        unique.sort(key=lambda r: (r.cost, -r.reliability))
        return unique[:10]
