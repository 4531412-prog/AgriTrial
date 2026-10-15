
# app/metrics.py

MEASUREMENT_FIELDS = frozenset({
    "yield",
    "bio_yield",
    "pods_per_plant",
    "thousand_seed_wt",
    "oil_pct",
    "n",
    "p",
    "k",
    "na",
    "ca",
    "mg",
    "fe",
    "mn",
    "zn",
    "cu",
    "chl_a",
    "chl_b",
    "rwc",
    "ionic_leakage",
    "proline",
})


def validate_metric(metric: str) -> str:
    if metric not in MEASUREMENT_FIELDS:
        raise ValueError(
            f"Unsupported measurement: {metric}"
        )

    return metric
