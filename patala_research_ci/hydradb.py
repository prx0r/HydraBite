"""HydraDB adapter — replaces OpenAIRE adapter for Hack Hydra."""
import httpx
from typing import Any

HYDRADB_MCP = "https://mcp.hydradb.com/mcp"

class HydraDB:
    """HydraDB MCP client."""

    def __init__(self, mcp_url: str = HYDRADB_MCP):
        self.url = mcp_url
        self.c = httpx.Client(timeout=30)

    def _call(self, tool: str, args: dict) -> dict:
        r = self.c.post(self.url, json={
            "method": "tools/call",
            "params": {"name": tool, "arguments": args}
        })
        r.raise_for_status()
        return r.json()

    def query(self, text: str, mode: str = "fast") -> dict:
        """Search memories and knowledge with graph context."""
        return self._call("hydradb_query", {"query": text, "mode": mode})

    def ingest(self, text: str, title: str = "", is_markdown: bool = True) -> dict:
        """Store content as a memory/knowledge source."""
        return self._call("hydradb_ingest", {
            "text": text, "title": title, "is_markdown": is_markdown
        })

    def list_memories(self) -> dict:
        """List all memories."""
        return self._call("hydradb_list", {"kind": "memory"})

    def list_sources(self) -> dict:
        """List all knowledge sources."""
        return self._call("hydradb_list", {"kind": "knowledge"})

    def inspect(self, source_id: str) -> dict:
        """Get full content of a source."""
        return self._call("hydradb_inspect", {"id": source_id})

    def graph_query(self, cypher: str, params: dict = None) -> dict:
        """Run Cypher query on knowledge graph."""
        args = {"query": cypher}
        if params:
            args["params"] = params
        return self._call("hydradb_graph_query", args)

    def graph_collections(self) -> dict:
        """List graph collections."""
        return self._call("hydradb_graph_collections", {})
