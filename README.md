# AgriTrial Backend

Backend API and statistical analysis module for the AgriTrial MVP.

## Project Purpose

AgriTrial is being developed to support the capture, validation,
analysis, and reporting of agricultural trial data.

This repository currently contains the backend and analytical
functionality used to retrieve trial observations, validate
comparisons, and calculate statistical results for the dashboard.

## Current Backend Features

The backend currently supports:

- FastAPI REST API
- Trial-data retrieval and filtering
- Two-treatment comparison
- Multiple-treatment comparison
- Cross-site comparison
- Scientific comparison validation
- Mean calculation
- Sample variance
- Standard deviation
- Standard error
- 95% confidence intervals
- Pydantic response models
- Automated pytest tests

## Development Data

The current records stored in `app/data.py` are synthetic
development fixture data.

They are included only for:

- backend development
- API testing
- statistical testing
- dashboard/frontend integration

They must not be interpreted as real agricultural trial results.

The synthetic data will later be replaced by the AgriTrial
SQLite/Supabase persistence layer.

## Project Structure

```text
agritrial-backend/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── data.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── statistics.py
│   └── validation.py
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_comparison.py
│   ├── test_statistics.py
│   └── test_validation.py
├── .gitignore
├── README.md
└── requirements.txt
