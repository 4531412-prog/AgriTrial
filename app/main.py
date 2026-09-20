
from app.data import TRIAL_DATA

from app.statistics import calculate_ci

from app.validation import (
    validate_comparison,
    validate_multi_site_comparison
)
from app.models import (
    ComparisonResponse,
    MultiSiteComparisonResponse
)
from fastapi import FastAPI, HTTPException, Query

from app.database import create_database, insert_obs
from app.models import Observations

app = FastAPI(
    title="AgriTrial API",
    description="Backend API for the AgriTrial MVP",
    version="0.1.0"
)

@app.on_event("startup") //added to insantiate the database 
def on_startup():
    create_database()

@app.post("/observations")
async def create_record(record: Observations):
    try:
        insert_obs(record)
    except Exception as e :
        raise HTTPException(status_code=500, detail=f"{e} is the reason.")
    return {"status": "success", "record": record}


@app.get("/")
def root():
    return {
        "name": "AgriTrial API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/trials")
def get_trials(
    site: str | None = None,
    treatment: str | None = None,
    crop: str | None = None,
    metric: str | None = None
):
    results = TRIAL_DATA

    if site:
        results = [
            row for row in results
            if row["site"] == site
        ]

    if treatment:
        results = [
            row for row in results
            if row["treatment"] == treatment
        ]

    if crop:
        results = [
            row for row in results
            if row["crop"] == crop
        ]

    if metric:
        results = [
            row for row in results
            if row["metric"] == metric
        ]

    return {
        "count": len(results),
        "data": results
    }
@app.get(
    "/compare",
    response_model=ComparisonResponse
)
def compare_treatments(
    site: str,
    crop: str,
    metric: str,
    treatment_a: str,
    treatment_b: str
):
    try:
        validate_comparison(
            data=TRIAL_DATA,
            site=site,
            crop=crop,
            metric=metric,
            treatments=[
                treatment_a,
                treatment_b
            ]
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    group_a = [
        row["value"]
        for row in TRIAL_DATA
        if row["site"] == site
        and row["crop"] == crop
        and row["metric"] == metric
        and row["treatment"] == treatment_a
    ]

    group_b = [
        row["value"]
        for row in TRIAL_DATA
        if row["site"] == site
        and row["crop"] == crop
        and row["metric"] == metric
        and row["treatment"] == treatment_b
    ]

    return {
        "site": site,
        "crop": crop,
        "metric": metric,
        "confidence_level": 0.95,
        "groups": [
            {
                "treatment": treatment_a,
                **calculate_ci(group_a)
            },
            {
                "treatment": treatment_b,
                **calculate_ci(group_b)
            }
        ]
    }
@app.get(
    "/compare-multiple",
    response_model=ComparisonResponse
)
def compare_multiple_treatments(
    site: str,
    crop: str,
    metric: str,
    treatments: list[str] = Query(...)
):
    try:
        validate_comparison(
            data=TRIAL_DATA,
            site=site,
            crop=crop,
            metric=metric,
            treatments=treatments
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    groups = []

    for treatment in treatments:
        values = [
            row["value"]
            for row in TRIAL_DATA
            if row["site"] == site
            and row["crop"] == crop
            and row["metric"] == metric
            and row["treatment"] == treatment
        ]

        groups.append(
            {
                "treatment": treatment,
                **calculate_ci(values)
            }
        )

    return {
        "site": site,
        "crop": crop,
        "metric": metric,
        "confidence_level": 0.95,
        "groups": groups
    }
@app.get(
    "/compare-sites",
    response_model=MultiSiteComparisonResponse
)
def compare_sites(
    crop: str,
    metric: str,
    treatment: str,
    sites: list[str] = Query(...)
):
    try:
        validate_multi_site_comparison(
            data=TRIAL_DATA,
            sites=sites,
            crop=crop,
            metric=metric,
            treatment=treatment
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    groups = []

    for site in sites:
        values = [
            row["value"]
            for row in TRIAL_DATA
            if row["site"] == site
            and row["crop"] == crop
            and row["metric"] == metric
            and row["treatment"] == treatment
        ]

        groups.append(
            {
                "site": site,
                "treatment": treatment,
                **calculate_ci(values)
            }
        )

    return {
        "sites": sites,
        "crop": crop,
        "metric": metric,
        "treatment": treatment,
        "confidence_level": 0.95,
        "groups": groups
    }
