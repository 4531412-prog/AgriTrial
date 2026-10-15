import pytest

from app.data import TRIAL_DATA
from app.validation import validate_comparison


def test_valid_comparison():
    result = validate_comparison(
        data=TRIAL_DATA,
        site="Site A",
        crop="Tomato",
        metric="nitrate",
        treatments=[
            "Control",
            "Treatment A"
        ]
    )

    assert result is True


def test_missing_treatment():
    with pytest.raises(
        ValueError,
        match="does not exist"
    ):
        validate_comparison(
            data=TRIAL_DATA,
            site="Site A",
            crop="Tomato",
            metric="nitrate",
            treatments=[
                "Control",
                "Treatment X"
            ]
        )


def test_duplicate_treatment():
    with pytest.raises(
        ValueError,
        match="must be different"
    ):
        validate_comparison(
            data=TRIAL_DATA,
            site="Site A",
            crop="Tomato",
            metric="nitrate",
            treatments=[
                "Control",
                "Control"
            ]
        )


def test_wrong_crop():
    with pytest.raises(
        ValueError,
        match="does not exist"
    ):
        validate_comparison(
            data=TRIAL_DATA,
            site="Site A",
            crop="Maize",
            metric="nitrate",
            treatments=[
                "Control",
                "Treatment A"
            ]
        )

def test_reject_missing_measurement_value():
    from app.validation import validate_comparison

    data = [
        {"site": "A", "crop": "Soybean", "metric": "yield",
         "treatment": "Control", "value": 10.0},
        {"site": "A", "crop": "Soybean", "metric": "yield",
         "treatment": "Control", "value": None},
        {"site": "A", "crop": "Soybean", "metric": "yield",
         "treatment": "Fertilizer", "value": 12.0},
        {"site": "A", "crop": "Soybean", "metric": "yield",
         "treatment": "Fertilizer", "value": 14.0},
    ]

    import pytest

    with pytest.raises(ValueError, match="valid observations"):
        validate_comparison(
            data=data,
            site="A",
            crop="Soybean",
            metric="yield",
            treatments=["Control", "Fertilizer"],
        )

def test_multi_site_rejects_missing_measurement():
    import pytest
    from app.validation import validate_multi_site_comparison

    data = [
        {"site": "A", "crop": "Soybean", "metric": "yield",
         "treatment": "Control", "value": 10.0},
        {"site": "A", "crop": "Soybean", "metric": "yield",
         "treatment": "Control", "value": None},
        {"site": "B", "crop": "Soybean", "metric": "yield",
         "treatment": "Control", "value": 12.0},
        {"site": "B", "crop": "Soybean", "metric": "yield",
         "treatment": "Control", "value": 14.0},
    ]

    with pytest.raises(ValueError, match="valid observations"):
        validate_multi_site_comparison(
            data=data,
            sites=["A", "B"],
            crop="Soybean",
            metric="yield",
            treatment="Control",
        )