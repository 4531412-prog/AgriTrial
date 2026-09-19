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

    if len(values) < 2:
        raise ValueError(
            "At least two observations are required "
            "to calculate a confidence interval."
        )

    data = np.array(values, dtype=float)

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

    lower, upper = stats.t.interval(
        confidence,
        df=n - 1,
        loc=mean,
        scale=standard_error
    )

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
