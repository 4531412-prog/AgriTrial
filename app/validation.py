def validate_comparison(
    data: list[dict],
    site: str,
    crop: str,
    metric: str,
    treatments: list[str],
    minimum_observations: int = 2
):
    """
    Validate whether treatment groups can be
    scientifically compared.
    """

    # Rule 1:
    # The requested site must exist.
    site_rows = [
        row for row in data
        if row["site"] == site
    ]

    if not site_rows:
        raise ValueError(
            f"Site '{site}' does not exist."
        )

    # Rule 2:
    # The requested crop must exist at the site.
    crop_rows = [
        row for row in site_rows
        if row["crop"] == crop
    ]

    if not crop_rows:
        raise ValueError(
            f"Crop '{crop}' does not exist "
            f"at site '{site}'."
        )

    # Rule 3:
    # The metric must exist for that crop.
    metric_rows = [
        row for row in crop_rows
        if row["metric"] == metric
    ]

    if not metric_rows:
        raise ValueError(
            f"Metric '{metric}' does not exist "
            f"for crop '{crop}' at site '{site}'."
        )

    # Rule 4:
    # At least two treatment groups are needed.
    if len(treatments) < 2:
        raise ValueError(
            "At least two treatment groups "
            "are required for comparison."
        )

    # Rule 5:
    # The same treatment should not be
    # compared against itself.
    if len(set(treatments)) != len(treatments):
        raise ValueError(
            "Treatment groups must be different."
        )

    # Rule 6:
    # Every requested treatment must exist
    # and contain enough observations.
    for treatment in treatments:
        treatment_rows = [
            row for row in metric_rows
            if row["treatment"] == treatment
        ]

        if not treatment_rows:
            raise ValueError(
                f"Treatment '{treatment}' "
                f"does not exist."
            )

        if len(treatment_rows) < minimum_observations:
            raise ValueError(
                f"Treatment '{treatment}' requires "
                f"at least {minimum_observations} "
                f"observations."
            )

    return True

def validate_multi_site_comparison(
    data: list[dict],
    sites: list[str],
    crop: str,
    metric: str,
    treatment: str,
    minimum_observations: int = 2
):
    """
    Validate whether the same treatment can be
    compared across multiple trial sites.
    """

    if len(sites) < 2:
        raise ValueError(
            "At least two sites are required "
            "for a multi-site comparison."
        )

    if len(set(sites)) != len(sites):
        raise ValueError(
            "Sites must be different."
        )

    for site in sites:
        site_rows = [
            row for row in data
            if row["site"] == site
        ]

        if not site_rows:
            raise ValueError(
                f"Site '{site}' does not exist."
            )

        crop_rows = [
            row for row in site_rows
            if row["crop"] == crop
        ]

        if not crop_rows:
            raise ValueError(
                f"Crop '{crop}' does not exist "
                f"at site '{site}'."
            )

        metric_rows = [
            row for row in crop_rows
            if row["metric"] == metric
        ]

        if not metric_rows:
            raise ValueError(
                f"Metric '{metric}' does not exist "
                f"for crop '{crop}' at site '{site}'."
            )

        treatment_rows = [
            row for row in metric_rows
            if row["treatment"] == treatment
        ]

        if not treatment_rows:
            raise ValueError(
                f"Treatment '{treatment}' does not "
                f"exist at site '{site}'."
            )

        if len(treatment_rows) < minimum_observations:
            raise ValueError(
                f"Treatment '{treatment}' at "
                f"site '{site}' requires at least "
                f"{minimum_observations} observations."
            )

    return True