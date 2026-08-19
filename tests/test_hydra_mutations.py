from hydrabite.hydra import HydraClient


class Capture(HydraClient):
    def __init__(self):
        super().__init__(); self.calls=[]
    def query(self, query, parameters=None, **kwargs):
        self.calls.append((query,parameters or {},kwargs))
        if "RETURN n.id AS id" in query:
            return [{"id": parameters["vertex"]}]
        if "RETURN r.id AS id" in query:
            return [{"id": parameters["rid"]}]
        return []


def test_vertex_upsert_uses_hydra_documented_unwind_merge_set_then_strong_readback():
    c=Capture(); c.upsert_vertex("HBClaim",42,{"claim_key":"x","trust":"VERIFIED"})
    mutation,params,_=c.calls[0]
    assert mutation.startswith("UNWIND $rows AS row MERGE (n {id: row.vertex}) SET n:HBClaim")
    assert params["rows"][0]["vertex"]==42
    assert c.calls[1][2]["consistency"]=="strong"


def test_edge_upsert_uses_matched_merge_with_relationship_id_and_readback():
    c=Capture(); rid=c.merge_edge(1,"VERIFIED_BY",2)
    mutation,params,_=c.calls[0]
    assert "UNWIND $rows AS row MATCH (s {id: row.src}), (d {id: row.dst})" in mutation
    assert "MERGE (s)-[r:VERIFIED_BY {id: row.relationship_vertex}]->(d)" in mutation
    assert "SET r.edge_key = row.edge_key" in mutation
    assert params["rows"][0]["relationship_vertex"]==rid
    assert c.calls[1][2]["consistency"]=="strong"
