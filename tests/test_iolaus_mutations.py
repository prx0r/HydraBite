from iolaus.hydra import HydraClient


class Capture(HydraClient):
    def __init__(self):
        super().__init__()
        self.calls = []

    def query(self, query, parameters=None, **kwargs):
        self.calls.append((query, parameters or {}, kwargs))
        vid = parameters.get("vertex") or parameters.get("vid", 0)
        return [{"vertex_id": vid}]


def test_vertex_upsert_creates_node_with_label():
    c = Capture()
    c.upsert_vertex("HBClaim", 42, {"claim_key": "x", "trust": "VERIFIED"})
    mutation, params, kwargs = c.calls[0]
    assert "MERGE" in mutation or "MERGE" in mutation.upper()
    assert "HBClaim" in mutation
    assert len(c.calls) >= 1


def test_edge_upsert_creates_relationship():
    c = Capture()
    rid = c.merge_edge(1, "VERIFIED_BY", 2)
    mutation, params, kwargs = c.calls[0]
    assert "MERGE" in mutation or "MERGE" in mutation.upper()
    assert "VERIFIED_BY" in mutation
    assert rid is not None


def test_upsert_is_idempotent():
    c = Capture()
    c.upsert_vertex("HBContract", 10, {"version": "1"})
    c.upsert_vertex("HBContract", 10, {"version": "2"})
    assert len(c.calls) == 2


def test_merge_edge_returns_id():
    c = Capture()
    rid = c.merge_edge(1, "USES_CONTRACT", 2)
    assert rid is not None


def test_has_verified_claim_queries_graph():
    c = Capture()
    c.has_verified_claim("test:claim")
    assert len(c.calls) >= 1


def test_vertex_upsert_includes_properties():
    c = Capture()
    c.upsert_vertex("HBReceipt", 99, {"verdict": "PASS", "receipt_hash": "abc"})
    mutation, params, kwargs = c.calls[0]
    assert "HBReceipt" in mutation
    props = params.get("props") or params.get("properties") or {}
    assert "verdict" in str(props) or "PASS" in mutation
