from pydantic import BaseModel


class TreatmentStatistics(BaseModel):
    treatment: str
    n: int
    mean: float
    variance: float
    standard_deviation: float
    standard_error: float
    ci95_lower: float
    ci95_upper: float


class ComparisonResponse(BaseModel):
    site: str
    crop: str
    metric: str
    confidence_level: float
    groups: list[TreatmentStatistics]


class SiteStatistics(BaseModel):
    site: str
    treatment: str
    n: int
    mean: float
    variance: float
    standard_deviation: float
    standard_error: float
    ci95_lower: float
    ci95_upper: float


class MultiSiteComparisonResponse(BaseModel):
    sites: list[str]
    crop: str
    metric: str
    treatment: str
    confidence_level: float
    groups: list[SiteStatistics]