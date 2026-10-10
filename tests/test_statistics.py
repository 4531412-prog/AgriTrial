import pytest

from app.statistics import calculate_ci


def test_calculate_ci():
    values = [20.1, 21.7, 22.4]

    result = calculate_ci(values)

    assert result["n"] == 3
    assert result["mean"] == pytest.approx(
        21.4,
        abs=0.0001
    )

    assert result["variance"] > 0
    assert result["standard_deviation"] > 0
    assert result["standard_error"] > 0

    assert result["ci95_lower"] < result["mean"]
    assert result["ci95_upper"] > result["mean"]


def test_ci_requires_two_observations():
    with pytest.raises(ValueError):
        calculate_ci([20.1])

import pytest


def test_identical_measurements():
    from app.statistics import calculate_ci

    result = calculate_ci([10, 10, 10])

    assert result["mean"] == 10.0
    assert result["standard_error"] == 0.0
    assert result["ci95_lower"] == 10.0
    assert result["ci95_upper"] == 10.0


def test_reject_nan_measurement():
    from app.statistics import calculate_ci

    with pytest.raises(
        ValueError,
        match="All observations must be valid, finite numbers"
    ):
        calculate_ci([10, float("nan"), 14])


def test_reject_infinite_measurement():
    from app.statistics import calculate_ci

    with pytest.raises(
        ValueError,
        match="All observations must be valid, finite numbers"
    ):
        calculate_ci([10, float("inf"), 14])


def test_reject_invalid_confidence():
    from app.statistics import calculate_ci

    with pytest.raises(
        ValueError,
        match="Confidence level must be between 0 and 1"
    ):
        calculate_ci([10, 12, 14], confidence=1.5)