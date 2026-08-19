import math
import pytest
from iolaus.canonical import canonical_bytes, sha256_hex


def test_canonical_hash_is_order_independent():
    assert canonical_bytes({"b": 2, "a": 1}) == canonical_bytes({"a": 1, "b": 2})
    assert sha256_hex({"b": 2, "a": 1}) == sha256_hex({"a": 1, "b": 2})


def test_nonfinite_values_rejected():
    with pytest.raises(ValueError):
        canonical_bytes({"x": math.nan})
