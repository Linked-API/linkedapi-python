from __future__ import annotations

from typing import Literal

from linkedapi.types.base import LinkedApiModel
from linkedapi.types.params import BaseActionParams, LimitParams

SearchCompanySize = Literal[
    "1-10",
    "11-50",
    "51-200",
    "201-500",
    "501-1000",
    "1001-5000",
    "5001-10000",
    "10001+",
]
MinAnnualRevenue = Literal["0", "0.5", "1", "2.5", "5", "10", "20", "50", "100", "500", "1000"]
MaxAnnualRevenue = Literal[
    "0.5",
    "1",
    "2.5",
    "5",
    "10",
    "20",
    "50",
    "100",
    "500",
    "1000",
    "1000+",
]


class SearchCompaniesFilter(LinkedApiModel):
    sizes: list[SearchCompanySize] | None = None
    locations: list[str] | None = None
    industries: list[str] | None = None


class SearchCompaniesParams(BaseActionParams, LimitParams):
    term: str | None = None
    filter: SearchCompaniesFilter | None = None
    custom_search_url: str | None = None


class SearchCompanyResult(LinkedApiModel):
    name: str | None = None
    public_url: str | None = None
    industry: str | None = None
    location: str | None = None


class AnnualRevenueFilter(LinkedApiModel):
    min: MinAnnualRevenue
    max: MaxAnnualRevenue


class NvSearchCompaniesFilter(SearchCompaniesFilter):
    annual_revenue: AnnualRevenueFilter | None = None


class NvSearchCompaniesParams(BaseActionParams, LimitParams):
    term: str | None = None
    filter: NvSearchCompaniesFilter | None = None
    custom_search_url: str | None = None


class NvSearchCompanyResult(LinkedApiModel):
    name: str | None = None
    hashed_url: str | None = None
    industry: str | None = None
    employees_count: int | None = None
