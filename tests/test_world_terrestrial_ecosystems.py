"""Tests for the world_terrestrial_ecosystems module."""

from tests.conftest import load_response
from geoenvo.data_sources.world_terrestrial_ecosystems import apply_code_mapping


def test_apply_code_mapping():
    """Test apply_code_mapping function."""

    # Positive test case - Code of a non-empty response are mapped to
    # environmental properties
    response = load_response("wte_success")
    code = response.data["properties"]["Values"][0]
    assert code == "175"
    data = apply_code_mapping(response.data)
    assert len(data["results"]) == 1
    for k, v in data["results"][0].items():
        assert isinstance(k, str)
        assert len(k) > 0
        assert isinstance(v, str)
        assert len(v) > 0

    # Negative test case - Codes of an empty response are not mapped to
    # environmental properties
    response = load_response("wte_fail")
    code = response.data["properties"]["Values"][0]
    assert code == "NoData"
    data = apply_code_mapping(response.data)
    assert data == {"results": []}
