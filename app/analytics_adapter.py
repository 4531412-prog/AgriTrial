# app/analytics_adapter.py

from app.metrics import MEASUREMENT_FIELDS


def normalize_observations(observations):
    """Convert wide agricultural observations to metric/value rows."""

    normalized = []

    for observation in observations:
        for metric in sorted(MEASUREMENT_FIELDS):
            normalized.append({
                "site": observation.get("site"),
                "crop": observation.get("crop"),
                "treatment": observation.get("treatment"),
                "year": observation.get("year"),
                "rep": observation.get("rep"),
                "metric": metric,
                "value": observation.get(metric),
            })

    return normalized


def get_live_analytical_data():
    """Retrieve and normalize agricultural observations from Supabase."""

    from app.database import supabase

    fields = ",".join(sorted(MEASUREMENT_FIELDS))

    selection = (
        fields
        + ",year,rep,"
        + "treatments(name,trials(crop,sites(name)))"
    )

    response = (
        supabase.table("observations")
        .select(selection)
        .execute()
    )

    observations = []

    for row in response.data:
        treatment = row.get("treatments")

        if not isinstance(treatment, dict):
            continue

        trial = treatment.get("trials")

        if not isinstance(trial, dict):
            continue

        site = trial.get("sites")

        if not isinstance(site, dict):
            continue

        observation = {
            "site": site.get("name"),
            "crop": trial.get("crop"),
            "treatment": treatment.get("name"),
            "year": row.get("year"),
            "rep": row.get("rep"),
        }

        for metric in MEASUREMENT_FIELDS:
            observation[metric] = row.get(metric)

        observations.append(observation)

    return normalize_observations(observations)