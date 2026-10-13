from app.analytics_adapter import normalize_observations
from app.metrics import MEASUREMENT_FIELDS


def test_all_20_metrics_are_generated():
    observations = [{
        "site": "Site A",
        "crop": "Canola",
        "treatment": "Control",
        "yield": 3.5,
        "oil_pct": 42.1,
    }]

    result = normalize_observations(observations)

    assert len(result) == 20
    assert {row["metric"] for row in result} == MEASUREMENT_FIELDS


def test_measurement_values_are_preserved():
    observations = [{
        "site": "Site A",
        "crop": "Canola",
        "treatment": "Control",
        "yield": 3.5,
        "oil_pct": 42.1,
    }]

    result = normalize_observations(observations)

    values = {row["metric"]: row["value"] for row in result}

    assert values["yield"] == 3.5
    assert values["oil_pct"] == 42.1
    assert values["proline"] is None


def test_empty_observations():
    assert normalize_observations([]) == []


def test_multiple_observations():
    observations = [
        {"site": "A", "yield": 3.5},
        {"site": "B", "yield": 4.2},
    ]

    result = normalize_observations(observations)

    assert len(result) == 40
    assert sum(row["metric"] == "yield" for row in result) == 2

from unittest.mock import MagicMock, patch

from app.analytics_adapter import get_live_analytical_data


def test_live_retrieval_normalizes_supabase_records():
    fake_record = {
        "year": 2026,
        "rep": 1,
        "yield": 1800.0,
        "oil_pct": 42.0,
        "treatments": {
            "name": "Control",
            "trials": {
                "crop": "Canola",
                "sites": {"name": "Test Site"},
            },
        },
    }

    fake_client = MagicMock()
    fake_client.table.return_value.select.return_value.execute.return_value.data = [
        fake_record
    ]

    with patch("app.database.supabase", fake_client):
        result = get_live_analytical_data()

    assert len(result) == 20

    yield_record = next(
        row for row in result if row["metric"] == "yield"
    )

    assert yield_record["site"] == "Test Site"
    assert yield_record["crop"] == "Canola"
    assert yield_record["treatment"] == "Control"
    assert yield_record["value"] == 1800.0
    assert yield_record["year"] == 2026
    assert yield_record["rep"] == 1


def test_live_retrieval_skips_missing_relationships():
    fake_client = MagicMock()
    fake_client.table.return_value.select.return_value.execute.return_value.data = [
        {"treatments": None, "yield": 1000.0}
    ]

    with patch("app.database.supabase", fake_client):
        result = get_live_analytical_data()

    assert result == []