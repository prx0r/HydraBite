"""CLI for HydraBite."""
import sys
from . import HydraBite, Bite, Status


def main():
    import argparse
    p = argparse.ArgumentParser(prog="hydrabite", description="Verified state transitions for agents")
    sub = p.add_subparsers(dest="command")

    d = sub.add_parser("demo", help="Run the demo")
    s = sub.add_parser("status", help="Show current state")
    args = p.parse_args()

    if args.command == "demo":
        from .demo import main as demo_main
        demo_main()
    elif args.command == "status":
        print("No active bites.")
    else:
        p.print_help()
