#!/usr/bin/env python3
"""Search the OpenAIRE Graph API — V4 unified filters."""

import httpx
import json
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

V4_BASE = "https://api-beta.openaire.eu/graph/v4"


def search_research_products(query: str, filters: dict = None, page_size: int = 5):
    """Search research products with V4 unified filter syntax."""
    params = {"search": query, "page_size": page_size}
    if filters:
        filter_parts = [f"{k}:{v}" for k, v in filters.items()]
        params["filter"] = ",".join(filter_parts)

    r = httpx.get(f"{V4_BASE}/research-products", params=params, timeout=15)
    r.raise_for_status()
    return r.json()


def print_results(data: dict):
    """Pretty-print search results."""
    header = data.get("header", {})
    results = data.get("results", [])

    console.print(f"  Found [bold]{header.get('numFound', '?')}[/bold] results "
                  f"(page {header.get('page', '?')}, "
                  f"query {header.get('queryTime', '?')}ms)")

    if not results:
        console.print("  No results.")
        return

    table = Table(title="Results")
    table.add_column("Type", style="cyan", width=12)
    table.add_column("Title", max_width=60)
    table.add_column("Date", width=12)
    table.add_column("OA", width=6)

    for rp in results:
        rp_type = rp.get("type", "?")
        title = rp.get("mainTitle", rp.get("title", "?"))
        if len(title) > 55:
            title = title[:52] + "..."
        date = rp.get("publicationDate", "?")
        oa = (rp.get("bestAccessRight") or {}).get("label", "?")[:6]
        table.add_row(rp_type, title, date, oa)

    console.print(table)


def search_with_facets(query: str, facet_fields: list, page_size: int = 0):
    """Search with aggregations/facets only (no records)."""
    params = {
        "search": query,
        "facets": ",".join(facet_fields),
        "page_size": page_size,
    }
    r = httpx.get(f"{V4_BASE}/research-products", params=params, timeout=15)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[bold]Usage:[/bold] python search.py <query> [--facets] [--type TYPE] [--oa RIGHTS] [--year YEAR]")
        console.print()
        console.print("Examples:")
        console.print("  python search.py 'open access'")
        console.print("  python search.py 'machine learning' --type publication --year 2024")
        console.print("  python search.py 'climate change' --facets")
        sys.exit(1)

    query = sys.argv[1]
    show_facets = "--facets" in sys.argv

    filters = {}
    for i, arg in enumerate(sys.argv):
        if arg == "--type" and i + 1 < len(sys.argv):
            filters["type"] = sys.argv[i + 1]
        if arg == "--oa" and i + 1 < len(sys.argv):
            filters["best_oa.rights"] = sys.argv[i + 1]
        if arg == "--year" and i + 1 < len(sys.argv):
            filters["from_publication_year"] = sys.argv[i + 1]

    if show_facets:
        console.print(Panel(f"[bold cyan]Facets for: {query}[/bold cyan]"))
        data = search_with_facets(query, ["type", "best_oa.rights", "language"])
        console.print_json(json.dumps(data, indent=2))
    else:
        console.print(Panel(f"[bold cyan]Search: {query}[/bold cyan]"))
        data = search_research_products(query, filters)
        print_results(data)
