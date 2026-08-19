"""Engine policy tests use a deliberately tiny recording adapter, not as a Hydra substitute.

These tests exercise Python policy only. They are not accepted as Hydra integration evidence;
that lives under tests/integration and must hit the OSS graph-node.
"""
from hydrabite.engine import HydraBiteEngine, IntegrityViolation, UnauthorizedVerifier
from hydrabite.hydra import stable_vertex_id
from hydrabite.models import Contract, VerifierClass
from hydrabite.receipts import ReceiptSigner
from hydrabite.verifiers import CallableVerifier
import pytest


class RecordingHydra:
    def __init__(self):
        self.claims=set(); self.vertices={}; self.edges=[]; self.queries=[]
    def upsert_vertex(self,label,vertex_id,properties):
        self.vertices[vertex_id]=(label,dict(properties))
        if label=="HBClaim": self.claims.add(properties["claim_key"])
        return vertex_id
    def merge_edge(self,src,rel_type,dst,**kwargs):
        self.edges.append((src,rel_type,dst,kwargs)); return len(self.edges)
    def query(self,q,p=None,**kw):
        self.queries.append((q,p or {},kw))
        if "MATCH (c:HBClaim" in q and "claim_key" in (p or {}):
            return [{"claim_key":p["claim_key"]}] if p["claim_key"] in self.claims else []
        return [{"ok":1}]
    def has_verified_claim(self,k): return k in self.claims


def contract():
    return Contract(contract_id="c",description="c",produces_claim_templates=("done:{id}",),allowed_verifier_ids=("v",))


def test_failed_verification_does_not_create_claim():
    h=RecordingHydra(); e=HydraBiteEngine(h,ReceiptSigner.generate())
    p=e.execute(contract(),lambda a:{"success":True},{"id":"1"})
    v=CallableVerifier("v",VerifierClass.DETERMINISTIC_READBACK,lambda a,o:(False,"no",{}))
    r=e.verify(contract(),p,v)
    assert r.status.value=="REJECTED"
    assert "done:1" not in h.claims


def test_pass_verification_creates_claim():
    h=RecordingHydra(); e=HydraBiteEngine(h,ReceiptSigner.generate())
    p=e.execute(contract(),lambda a:{"success":True},{"id":"1"})
    v=CallableVerifier("v",VerifierClass.DETERMINISTIC_READBACK,lambda a,o:(True,"yes",{}))
    r=e.verify(contract(),p,v)
    assert r.status.value=="VERIFIED"
    assert "done:1" in h.claims
    assert stable_vertex_id("claim","done:1") in h.vertices


def test_contract_rejects_unauthorized_verifier():
    h=RecordingHydra(); e=HydraBiteEngine(h,ReceiptSigner.generate())
    p=e.execute(contract(),lambda a:{"success":True},{"id":"1"})
    v=CallableVerifier("evil",VerifierClass.HEURISTIC,lambda a,o:(True,"trust me",{}))
    with pytest.raises(UnauthorizedVerifier): e.verify(contract(),p,v)


def test_tampered_pending_output_is_rejected_before_promotion():
    h=RecordingHydra(); e=HydraBiteEngine(h,ReceiptSigner.generate())
    p=e.execute(contract(),lambda a:{"success":True},{"id":"1"})
    p.output={"success":False,"forged":True}
    v=CallableVerifier("v",VerifierClass.DETERMINISTIC_READBACK,lambda a,o:(True,"yes",{}))
    with pytest.raises(IntegrityViolation): e.verify(contract(),p,v)
    assert "done:1" not in h.claims
