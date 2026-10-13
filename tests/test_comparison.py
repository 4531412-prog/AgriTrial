
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from app.data import TRIAL_DATA
from app.main import app
from app.statistics import calculate_ci


# Keep the original synthetic observations, but use
# a metric supported by the production API.
TEST_DATA = [
    {**row, "metric": "yield"}
    for row in TRIAL_DATA
]

client = TestClient(app)


@pytest.fixture(autouse=True)
def use_synthetic_comparison_data():
    """Prevent comparison tests from accessing Supabase."""
    with patch(
        "app.main.get_live_analytical_data",
        return_value=TEST_DATA
    ):
        yield


def request_multiple(treatments, metric="yield"):
    return client.get(
        "/compare-multiple",
        params=[
            ("site", "Site A"),
            ("crop", "Tomato"),
            ("metric", metric),
            *[("treatments", t) for t in treatments],
        ],
    )


def request_sites(sites, metric="yield"):
    return client.get(
        "/compare-sites",
        params=[
            ("crop", "Tomato"),
            ("metric", metric),
            ("treatment", "Control"),
            *[("sites", site) for site in sites],
        ],
    )


def test_compare_multiple_treatments():
    response = request_multiple(
        ["Control", "Treatment A", "Treatment B"]
    )

    assert response.status_code == 200, response.text
    result = response.json()

    assert result["site"] == "Site A"
    assert result["crop"] == "Tomato"
    assert result["metric"] == "yield"
    assert result["confidence_level"] == 0.95

    assert [
        group["treatment"]
        for group in result["groups"]
    ] == ["Control", "Treatment A", "Treatment B"]

    for group in result["groups"]:
        values = [
            row["value"]
            for row in TEST_DATA
            if row["site"] == "Site A"
            and row["crop"] == "Tomato"
            and row["metric"] == "yield"
            and row["treatment"] == group["treatment"]
        ]

        expected = calculate_ci(values)

        for key, value in expected.items():
            assert group[key] == pytest.approx(value)


def test_compare_multiple_requires_two_treatments():
    response = request_multiple(["Control"])
    assert response.status_code == 400


def test_compare_multiple_rejects_duplicate_treatments():
    response = request_multiple(["Control", "Control"])
    assert response.status_code == 400


def test_compare_sites():
    response = request_sites(["Site A", "Site B"])

    assert response.status_code == 200, response.text
    result = response.json()

    assert result["crop"] == "Tomato"
    assert result["metric"] == "yield"
    assert result["treatment"] == "Control"
    assert result["sites"] == ["Site A", "Site B"]
    assert result["confidence_level"] == 0.95

    assert len(result["groups"]) == 2

    for group in result["groups"]:
        values = [
            row["value"]
            for row in TEST_DATA
            if row["site"] == group["site"]
            and row["crop"] == "Tomato"
            and row["metric"] == "yield"
            and row["treatment"] == "Control"
        ]

        expected = calculate_ci(values)

        assert group["treatment"] == "Control"

        for key, value in expected.items():
            assert group[key] == pytest.approx(value)


def test_compare_sites_requires_two_sites():
    response = request_sites(["Site A"])
    assert response.status_code == 400


def test_compare_sites_rejects_duplicate_sites():
    response = request_sites(["Site A", "Site A"])
    assert response.status_code == 400


def test_compare_multiple_rejects_unsupported_metric():
    response = request_multiple(
        ["Control", "Treatment A"],
        metric="nitrate"
    )
    assert response.status_code == 400


def test_compare_sites_rejects_unsupported_metric():
    response = request_sites(
        ["Site A", "Site B"],
        metric="nitrate"
    )
    assert response.status_code == 400


def test_compare_sites_rejects_nonexistent_site():
    response = request_sites(
        ["Site A", "Nonexistent Site"]
    )
    assert response.status_code == 400


def test_compare_sites_handles_data_source_failure():
    with patch(
        "app.main.get_live_analytical_data",
        side_effect=RuntimeError("Database unavailable")
    ):
        response = request_sites(["Site A", "Site B"])

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Analytical data is temporarily unavailable."
    )


def test_compare_sites_rejects_wrong_crop():
    response = client.get(
        "/compare-sites",
        params=[
            ("crop", "Maize"),
            ("metric", "yield"),
            ("treatment", "Control"),
            ("sites", "Site A"),
            ("sites", "Site B"),
        ],
    )

    assert response.status_code == 400
