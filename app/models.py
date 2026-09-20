from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class Observations(BaseModel):
    #compulsory
    treatment_id: int
    plot_number: int = Field(ge=1)
    rep: int = Field(ge=1)
    device_id: str

    #optional
    plant_height_cm: Optional[Decimal] = Field(default=None, ge=0, le=4000, decimal_places=3)
    yield_kg_per_plot: Optional[Decimal] = Field(default=None, ge=0, le=200, decimal_places=3)
    spad: Optional[Decimal] = Field(default=None, ge=0.0, le=99.9, decimal_places=3)
    disease_pct: Optional[Decimal] = Field(default=None, ge=0, le=100, decimal_places=3 )
    root_mass_g: Optional[Decimal] = Field(default=None, ge=0, le=1000, decimal_places=3)


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
