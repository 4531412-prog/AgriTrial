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
