
import numpy as np
from scipy import stats


def calculate_ci(
    values: list[float],
    confidence: float = 0.95
):
    """
    Calculate summary statistics and a confidence interval
    for a treatment group's measurements.
    """

    # Require at least two observations
    if len(values) < 2:
        raise ValueError(
            "At least two observations are required "
            "to calculate a confidence interval."
        )

    # Convert observations into numerical data
    data = np.array(values, dtype=float)

    # Reject NaN and infinite values
    if not np.all(np.isfinite(data)):
        raise ValueError(
            "All observations must be valid, finite numbers."
        )

    # Check that the confidence level is valid
    if not 0 < confidence < 1:
        raise ValueError(
            "Confidence level must be between 0 and 1."
        )

    # Calculate summary statistics
    n = len(data)

    mean = float(np.mean(data))

    variance = float(
        np.var(data, ddof=1)
    )

    standard_deviation = float(
        np.std(data, ddof=1)
    )

    standard_error = float(
        stats.sem(data)
    )

    # Handle identical observations
    if standard_error == 0:
        lower = mean
        upper = mean
    else:
        lower, upper = stats.t.interval(
            confidence,
            df=n - 1,
            loc=mean,
            scale=standard_error
        )

    # Return the results
    return {
        "n": n,
        "mean": round(mean, 4),
        "variance": round(variance, 4),
        "standard_deviation": round(
            standard_deviation, 4
        ),
        "standard_error": round(
            standard_error, 4
        ),
        "ci95_lower": round(float(lower), 4),
        "ci95_upper": round(float(upper), 4)
    }
