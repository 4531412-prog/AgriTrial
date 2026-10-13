from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional

class Observations(BaseModel):
    # compulsory
    treatment_id: int
    year: int= Field(ge=1)
    rep: int = Field(ge=1)
    device_id: str

    yield_: Optional[Decimal] = Field(default=None, alias="yield", ge=0, decimal_places=3)
    bio_yield: Optional[Decimal] = Field(default=None, ge=0, decimal_places=3)
    pods_per_plant: Optional[Decimal] = Field(default=None, ge=0, decimal_places=3)
    thousand_seed_wt: Optional[Decimal] = Field(default=None, ge=0, decimal_places=3)
    oil_pct: Optional[Decimal] = Field(default=None, ge=0, le=100, decimal_places=3)

    n: Optional[Decimal] = Field(default=None, ge=0, decimal_places=3)
    p: Optional[Decimal] = Field(default=None, ge=0, decimal_places=3)
    k: Optional[Decimal] = Field(default=None, ge=0, decimal_places=3)
    na: Optional[Decimal] = Field(default=None, ge=0, decimal_places=3)
    ca: Optional[Decimal] = Field(default=None, ge=0, decimal_places=3)
    mg: Optional[Decimal] = Field(default=None, ge=0, decimal_places=3)
    fe: Optional[Decimal] = Field(default=None, ge=0, decimal_places=3)
    mn: Optional[Decimal] = Field(default=None, ge=0, decimal_places=3)
    zn: Optional[Decimal] = Field(default=None, ge=0, decimal_places=3)
    cu: Optional[Decimal] = Field(default=None, ge=0, decimal_places=3)

    chl_a: Optional[Decimal] = Field(default=None, ge=0, decimal_places=3)
    chl_b: Optional[Decimal] = Field(default=None, ge=0, decimal_places=3)
    rwc: Optional[Decimal] = Field(default=None, ge=0, le=100, decimal_places=3)
    ionic_leakage: Optional[Decimal] = Field(default=None, ge=0, le=100, decimal_places=3)
    proline: Optional[Decimal] = Field(default=None, ge=0, decimal_places=3)

    class Config:
        populate_by_name = True  # lets you construct with yield_= in Python, while JSON still uses "yield"


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
