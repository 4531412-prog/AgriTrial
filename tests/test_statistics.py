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