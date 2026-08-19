"""CLI for HydraRoute."""
import json
from .hydra import HydraRoute
from .schema import DEFAULT_TOOLS, ToolDef
from .planner import Planner

def main():
    import argparse
    p = argparse.ArgumentParser(prog="hydraroute", description="Agent toolchain compiler")
    sub = p.add_subparsers(dest="command")

    plan = sub.add_parser("plan")
    plan.add_argument("--have", required=True, help="Comma-separated capabilities you have")
    plan.add_argument("--want", required=True, help="Capability you want")
    plan.add_argument("--max-cost", type=float, default=1.0)
    plan.add_argument("--max-latency", type=float, default=30.0)
    plan.add_argument("--disable", nargs="*", default=[], help="Disable tools")

    tools_cmd = sub.add_parser("tools")
    args = p.parse_args()

    if args.command == "plan":
        run_plan(args)
    elif args.command == "tools":
        run_tools()
    else:
        p.print_help()

def run_plan(args):
    have = [h.strip() for h in args.have.split(",")]
    hydra = HydraRoute()
    planner = Planner(hydra)

    disabled = [d.strip() for d in args.disable]

    routes = planner.plan(
        have=have,
        want=args.want,
        tools=DEFAULT_TOOLS,
        max_cost=args.max_cost,
        max_latency=args.max_latency,
        disabled=disabled,
    )

    print(f"\nGOAL: {args.want}")
    print(f"HAVE: {', '.join(have)}")
    print(f"DISABLED: {', '.join(disabled) if disabled else 'none'}\n")

    if not routes:
        print("  No valid routes found.")
        return

    for i, route in enumerate(routes):
        print(f"Route #{i+1}")
        print(f"{'─' * 40}")
        for step in route.steps:
            print(f"  → {step}")
        print(f"\n  cost:        ${route.cost:.3f}")
        print(f"  est latency: {route.latency:.1f}s")
        print(f"  reliability: {route.reliability:.0%}")
        print()

def run_tools():
    print(f"Available tools: {len(DEFAULT_TOOLS)}\n")
    for t in DEFAULT_TOOLS:
        req = ", ".join(t.requires) if t.requires else "none"
        prod = ", ".join(t.produces) if t.produces else "none"
        print(f"  {t.name:<25} req: {req:<30} prod: {prod:<20} cost: ${t.cost:.3f}")

if __name__ == "__main__":
    main()
