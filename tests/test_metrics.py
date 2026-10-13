import pytest

from app.metrics import MEASUREMENT_FIELDS, validate_metric


def test_all_20_measurements_supported():
    assert len(MEASUREMENT_FIELDS) == 20

    for metric in MEASUREMENT_FIELDS:
        assert validate_metric(metric) == metric


def test_oil_yield_is_excluded():
    with pytest.raises(ValueError, match="Unsupported measurement"):
        validate_metric("oil_yield")


def test_k_na_ratio_is_excluded():
    with pytest.raises(ValueError, match="Unsupported measurement"):
        validate_metric("k_na_ratio")


def test_unknown_measurement_is_rejected():
    with pytest.raises(ValueError, match="Unsupported measurement"):
        validate_metric("unknown_metric")