"""Alternative: leaner OpenAIRE client with pydantic models.

From neverbrokeagain-research-ci — simpler, fewer abstractions.
"""

import httpx

V3 = "https://api.openaire.eu/graph/v3"


class OpenAIRE:
    def __init__(self):
        self.c = httpx.Client(timeout=30, headers={"Accept": "application/json"})

    def search(self, entity: str = "research-products", **params) -> dict:
        params.setdefault("pageSize", 20)
        r = self.c.get(f"{V3}/{entity}", params=params)
        r.raise_for_status()
        return r.json()

    def products(self, search: str = "", **filters) -> list[dict]:
        p = {"search": search, "pageSize": 100, "includeStats": "true"}
        for k, v in filters.items():
            if isinstance(v, str) and " " in v:
                p[k] = f'"{v}"'
            else:
                p[k] = v
        r = self.c.get(f"{V3}/research-products", params=p)
        r.raise_for_status()
        return r.json().get("results", [])

    def product(self, oid: str) -> dict:
        r = self.c.get(f"{V3}/research-products/{oid}")
        r.raise_for_status()
        return r.json()

    def projects(self, **filters) -> list[dict]:
        p = {"pageSize": 50}
        p.update(filters)
        r = self.c.get(f"{V3}/projects", params=p)
        r.raise_for_status()
        return r.json().get("results", [])

    def persons(self, **filters) -> list[dict]:
        p = {"pageSize": 50}
        p.update(filters)
        r = self.c.get(f"{V3}/persons", params=p)
        r.raise_for_status()
        return r.json().get("results", [])
