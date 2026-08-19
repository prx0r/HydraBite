#!/usr/bin/env python3
"""Explore the OpenAIRE Graph API — V3 and V4 endpoints."""

import httpx
import json
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

V3_BASE = "https://api.openaire.eu/graph/v3"
V4_BASE = "https://api-beta.openaire.eu/graph/v4"


def explore_v3():
    """Hit V3 endpoints and show what's available."""
    console.print(Panel("[bold cyan]OpenAIRE Graph API V3[/bold cyan]"))

    endpoints = {
        "Research Products": f"{V3_BASE}/research-products?pageSize=2",
        "Organizations": f"{V3_BASE}/organizations?pageSize=2",
        "Data Sources": f"{V3_BASE}/datasources?pageSize=2",
        "Projects": f"{V3_BASE}/projects?pageSize=2",
        "Persons": f"{V3_BASE}/persons?pageSize=2",
    }

    for name, url in endpoints.items():
        try:
            r = httpx.get(url, timeout=15)
            r.raise_for_status()
            data = r.json()
            total = data.get("header", {}).get("numFound", "?")
            console.print(f"  [green]OK[/green]  {name}: {total} total")
        except Exception as e:
            console.print(f"  [red]ERR[/red] {name}: {e}")


def explore_v4():
    """Hit V4 endpoints and show what's available."""
    console.print(Panel("[bold cyan]OpenAIRE Graph API V4 (BETA)[/bold cyan]"))

    endpoints = {
        "Research Products": f"{V4_BASE}/research-products?page_size=2",
        "Organizations": f"{V4_BASE}/organizations?page_size=2",
        "Projects": f"{V4_BASE}/projects?page_size=2",
        "Persons": f"{V4_BASE}/persons?page_size=2",
    }

    for name, url in endpoints.items():
        try:
            r = httpx.get(url, timeout=15)
            r.raise_for_status()
            data = r.json()
            total = data.get("header", {}).get("numFound", "?")
            console.print(f"  [green]OK[/green]  {name}: {total} total")
        except Exception as e:
            console.print(f"  [red]ERR[/red] {name}: {e}")


def show_sample_research_product():
    """Fetch one research product and pretty-print it."""
    console.print(Panel("[bold cyan]Sample Research Product (V3)[/bold cyan]"))
    url = f"{V3_BASE}/research-products?pageSize=1"
    try:
        r = httpx.get(url, timeout=15)
        r.raise_for_status()
        data = r.json()
        results = data.get("results", [])
        if results:
            console.print_json(json.dumps(results[0], indent=2))
        else:
            console.print("  No results")
    except Exception as e:
        console.print(f"  [red]ERR[/red]: {e}")


def show_v4_filter_examples():
    """Show V4 unified filter syntax examples."""
    console.print(Panel("[bold cyan]V4 Filter Syntax Examples[/bold cyan]"))
    examples = [
        ("Type: publication", "filter=type:publication"),
        ("Open Access", "filter=best_oa.rights:Open Access"),
        ("Year >= 2023", "filter=from_publication_year:2023"),
        ("Has dataset link", "filter=has_dataset:true"),
        ("Combine filters", "filter=type:publication,from_publication_year:2023,best_oa.rights:Open Access"),
        ("Search + filter", "search=climate change&filter=type:publication"),
        ("Facets/aggregations", "facets=type,best_oa.rights,from_publication_year"),
    ]
    table = Table(title="V4 Unified Filters")
    table.add_column("Description", style="cyan")
    table.add_column("Query Parameter", style="green")
    for desc, param in examples:
        table.add_row(desc, param)
    console.print(table)


def show_data_types():
    """Show the research product type vocabulary."""
    console.print(Panel("[bold cyan]Research Product Types[/bold cyan]"))
    table = Table(title="Types")
    table.add_column("Type", style="cyan")
    table.add_column("Description")
    table.add_row("publication", "Journal articles, conference papers, books, theses")
    table.add_row("data", "Datasets, with geolocations and versions")
    table.add_row("software", "Code repos with programming language, docs URLs")
    table.add_row("other", "Protocols, methods, other research outputs")
    console.print(table)

    console.print(Panel("[bold cyan]Access Rights[/bold cyan]"))
    table = Table(title="Access Rights (COAR vocabulary)")
    table.add_column("Code", style="cyan")
    table.add_column("Label")
    table.add_row("c_abf2", "OPEN")
    table.add_row("c_16cb", "EMBARGO")
    table.add_row("c_14cb", "CLOSED")
    table.add_row("c_16ec", "RESTRICTED")
    console.print(table)

    console.print(Panel("[bold cyan]Open Access Colors[/bold cyan]"))
    table = Table(title="OA Colors")
    table.add_column("Color", style="cyan")
    table.add_column("Meaning")
    table.add_row("gold", "Published in fully OA journal")
    table.add_row("hybrid", "Published in subscription journal, OA option")
    table.add_row("bronze", "Free to read but no open license")
    console.print(table)


if __name__ == "__main__":
    explore_v3()
    console.print()
    explore_v4()
    console.print()
    show_data_types()
    console.print()
    show_v4_filter_examples()
    console.print()
    show_sample_research_product()
