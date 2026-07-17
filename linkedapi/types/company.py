from __future__ import annotations

from typing import Literal, TypeAlias

from pydantic import Field

from linkedapi.types.base import LinkedApiModel
from linkedapi.types.params import BaseActionParams, LimitParams, LimitSinceParams
from linkedapi.types.person import YearsOfExperience
from linkedapi.types.post import Post


class StCompanyEmployee(LinkedApiModel):
    name: str | None = None
    public_url: str | None = None
    headline: str | None = None
    location: str | None = None


class StCompanyDm(LinkedApiModel):
    name: str | None = None
    public_url: str | None = None
    headline: str | None = None
    location: str | None = None
    country_code: str | None = None


class Company(LinkedApiModel):
    name: str | None = None
    public_url: str | None = None
    description: str | None = None
    location: str | None = None
    headquarters: str | None = None
    industry: str | None = None
    specialties: str | None = None
    website: str | None = None
    employees_count: int | None = None
    year_founded: int | None = None
    venture_financing: bool | None = None
    jobs_count: int | None = None
    logo_url: str | None = None
    employees: list[StCompanyEmployee] | None = None
    dms: list[StCompanyDm] | None = None
    posts: list[Post] | None = None


class BaseFetchCompanyParams(BaseActionParams):
    company_url: str
    retrieve_employees: bool | None = None
    retrieve_dms: bool | None = Field(default=None, alias="retrieveDMs")
    retrieve_posts: bool | None = None


class BaseFetchCompanyParamsWide(BaseFetchCompanyParams):
    retrieve_employees: Literal[True] = True
    retrieve_dms: Literal[True] = Field(default=True, alias="retrieveDMs")
    retrieve_posts: Literal[True] = True


class StCompanyEmployeesFilter(LinkedApiModel):
    first_name: str | None = None
    last_name: str | None = None
    position: str | None = None
    locations: list[str] | None = None
    industries: list[str] | None = None
    schools: list[str] | None = None


class StCompanyEmployeesRetrievalConfig(LimitParams):
    filter: StCompanyEmployeesFilter | None = None


class FetchCompanyParams(BaseFetchCompanyParams):
    employees_retrieval_config: StCompanyEmployeesRetrievalConfig | None = None
    dms_retrieval_config: LimitParams | None = Field(default=None, alias="dmsRetrievalConfig")
    posts_retrieval_config: LimitSinceParams | None = None


FetchCompanyResult: TypeAlias = Company


class NvCompanyEmployee(LinkedApiModel):
    name: str | None = None
    hashed_url: str | None = None
    position: str | None = None
    location: str | None = None


class NvCompanyDm(LinkedApiModel):
    name: str | None = None
    hashed_url: str | None = None
    position: str | None = None
    location: str | None = None
    country_code: str | None = None


class NvCompany(LinkedApiModel):
    name: str | None = None
    public_url: str | None = None
    description: str | None = None
    location: str | None = None
    headquarters: str | None = None
    industry: str | None = None
    website: str | None = None
    employees_count: int | None = None
    year_founded: int | None = None
    logo_url: str | None = None
    employees: list[NvCompanyEmployee] | None = None
    dms: list[NvCompanyDm] | None = None


class NvBaseFetchCompanyParams(BaseActionParams):
    company_hashed_url: str
    retrieve_employees: bool | None = None
    retrieve_dms: bool | None = Field(default=None, alias="retrieveDMs")


class NvBaseFetchCompanyParamsWide(NvBaseFetchCompanyParams):
    retrieve_employees: Literal[True] = True
    retrieve_dms: Literal[True] = Field(default=True, alias="retrieveDMs")


class NvCompanyEmployeeFilter(LinkedApiModel):
    first_name: str | None = None
    last_name: str | None = None
    positions: list[str] | None = None
    locations: list[str] | None = None
    industries: list[str] | None = None
    schools: list[str] | None = None
    years_of_experiences: list[YearsOfExperience] | None = None


class NvCompanyEmployeeRetrievalConfig(LimitParams):
    filter: NvCompanyEmployeeFilter | None = None


class NvFetchCompanyParams(NvBaseFetchCompanyParams):
    employees_retrieval_config: NvCompanyEmployeeRetrievalConfig | None = None
    dms_retrieval_config: LimitParams | None = Field(default=None, alias="dmsRetrievalConfig")


NvFetchCompanyResult: TypeAlias = NvCompany
