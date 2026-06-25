from __future__ import annotations

from typing import Literal, TypeAlias

from linkedapi.types.base import LinkedApiModel
from linkedapi.types.params import BaseActionParams, LimitParams

JobDatePosted = Literal["anyTime", "past24Hours", "pastWeek", "pastMonth"]
JobExperienceLevel = Literal[
    "internship",
    "entryLevel",
    "associate",
    "midSeniorLevel",
    "director",
    "executive",
]
JobEmploymentType = Literal[
    "fullTime",
    "partTime",
    "contract",
    "temporary",
    "volunteer",
    "internship",
    "other",
]
JobWorkplaceType = Literal["onSite", "remote", "hybrid"]
SalaryPeriod = Literal["yearly", "monthly", "hourly"]
JobCurrency = Literal[
    "usd",
    "eur",
    "gbp",
    "inr",
    "cad",
    "aud",
    "nzd",
    "hkd",
    "sgd",
    "jpy",
    "cny",
    "chf",
    "sek",
    "nok",
    "dkk",
    "pln",
    "czk",
    "huf",
    "ron",
    "brl",
    "mxn",
    "ars",
    "zar",
    "aed",
    "sar",
    "ils",
    "try",
    "rub",
    "uah",
    "krw",
    "thb",
    "idr",
    "myr",
    "php",
    "vnd",
    "ngn",
    "twd",
]


class JobSalary(LinkedApiModel):
    currency: JobCurrency | None = None
    min_amount: float | None = None
    max_amount: float | None = None
    period: SalaryPeriod | None = None


class SearchJobsFilter(LinkedApiModel):
    location: str | None = None
    date_posted: JobDatePosted | None = None
    experience_levels: list[JobExperienceLevel] | None = None
    employment_types: list[JobEmploymentType] | None = None
    workplace_types: list[JobWorkplaceType] | None = None
    companies: list[str] | None = None
    industries: list[str] | None = None
    job_functions: list[str] | None = None
    easy_apply: bool | None = None
    has_verifications: bool | None = None
    under_10_applicants: bool | None = None
    in_your_network: bool | None = None
    fair_chance_employer: bool | None = None


class SearchJobsParams(BaseActionParams, LimitParams):
    term: str | None = None
    filter: SearchJobsFilter | None = None
    custom_search_url: str | None = None


class SearchJobResult(LinkedApiModel):
    job_id: str | None = None
    job_url: str | None = None
    title: str | None = None
    company_name: str | None = None
    location: str | None = None
    workplace_type: str | None = None
    salary: JobSalary | None = None
    easy_apply: bool | None = None
    is_promoted: bool | None = None


class FetchJobParams(BaseActionParams):
    job_url: str


class Job(LinkedApiModel):
    job_id: str | None = None
    job_url: str | None = None
    title: str | None = None
    company_name: str | None = None
    company_url: str | None = None
    location: str | None = None
    posted_date: str | None = None
    applicants_count: int | None = None
    workplace_type: str | None = None
    employment_type: str | None = None
    salary: JobSalary | None = None
    description: str | None = None
    apply_url: str | None = None
    easy_apply: bool | None = None


FetchJobResult: TypeAlias = Job
