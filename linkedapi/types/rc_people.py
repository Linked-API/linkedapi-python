from __future__ import annotations

from typing import Literal

from pydantic import Field

from linkedapi.types.base import LinkedApiModel
from linkedapi.types.params import BaseActionParams

RcEmploymentScope = Literal["currentOrPast", "current", "pastNotCurrent", "past"]
RcLocationScope = Literal["current", "currentOrOpenToRelocate", "openToRelocateOnly"]
RcCompanySize = Literal[
    "selfEmployed",
    "1-10",
    "11-50",
    "51-200",
    "201-500",
    "501-1000",
    "1001-5000",
    "5001-10000",
    "10001+",
]
RcJobFunction = Literal[
    "Accounting",
    "Administrative",
    "Arts and Design",
    "Business Development",
    "Community and Social Services",
    "Consulting",
    "Customer Success and Support",
    "Education",
    "Engineering",
    "Entrepreneurship",
    "Finance",
    "Healthcare Services",
    "Human Resources",
    "Information Technology",
    "Legal",
    "Marketing",
    "Media and Communication",
    "Military and Protective Services",
    "Operations",
    "Product Management",
    "Program and Project Management",
    "Purchasing",
    "Quality Assurance",
    "Real Estate",
    "Research",
    "Sales",
]
RcSeniority = Literal[
    "unpaid",
    "training",
    "entry",
    "senior",
    "manager",
    "director",
    "vp",
    "cxo",
    "partner",
    "owner",
]
RcNetworkRelationship = Literal["1st", "2nd", "groupMembers", "3rd+"]
RcRecentlyJoined = Literal["1day", "2to7days", "8to14days", "15to30days", "1to3months"]
RcRecruitingActivityType = Literal["messages", "notes", "projects", "resumes", "reviews"]
RcRecruitingActivityPeriod = Literal[
    "anytime",
    "pastDay",
    "pastWeek",
    "pastTwoWeeks",
    "pastThreeMonths",
    "pastSixMonths",
    "pastYear",
    "pastTwoYears",
]


class RcExperienceYears(LinkedApiModel):
    from_: int | None = Field(default=None, alias="from", ge=0, le=30)
    to: int | None = Field(default=None, ge=0, le=30)


class RcGraduationYears(LinkedApiModel):
    from_: int | None = Field(default=None, alias="from", ge=1900, le=2100)
    to: int | None = Field(default=None, ge=1900, le=2100)


class RcPostalCode(LinkedApiModel):
    code: str
    radius_miles: Literal[1, 5, 10, 25, 50, 100, 200] | None = None


class RcRecruitingActivityFilter(LinkedApiModel):
    type: RcRecruitingActivityType
    period: RcRecruitingActivityPeriod | None = None


class RcSearchPeopleFilter(LinkedApiModel):
    job_titles: list[str] | None = None
    locations: list[str] | None = None
    skills: list[str] | None = None
    companies: list[str] | None = None
    current_companies: list[str] | None = None
    past_companies: list[str] | None = None
    schools: list[str] | None = None
    industries: list[str] | None = None
    first_names: list[str] | None = None
    last_names: list[str] | None = None
    groups: list[str] | None = None
    projects: list[str] | None = None
    notes: list[str] | None = None
    job_titles_scope: RcEmploymentScope | None = None
    companies_scope: RcEmploymentScope | None = None
    locations_scope: RcLocationScope | None = None
    company_sizes: list[RcCompanySize] | None = None
    job_functions: list[RcJobFunction] | None = None
    seniority: list[RcSeniority] | None = None
    years_of_experience: RcExperienceYears | None = None
    profile_languages: list[str] | None = None
    network_relationships: list[RcNetworkRelationship] | None = None
    recently_joined: list[RcRecentlyJoined] | None = None
    has_passed_skill_assessment: bool | None = None
    is_military_veteran: bool | None = None
    hide_previously_viewed: bool | None = None
    postal_code: RcPostalCode | None = None
    graduation_years: RcGraduationYears | None = None
    recruiting_activity: RcRecruitingActivityFilter | None = None


class RcSearchPeopleParams(BaseActionParams):
    term: str | None = None
    filter: RcSearchPeopleFilter | None = None
    custom_search_url: str | None = None
    limit: int | None = Field(default=None, ge=1, le=1000)


class RcPersonViewerState(LinkedApiModel):
    connection_degree: Literal["1st", "2nd", "3rd+"] | str | None = None


class RcSearchPeopleResult(LinkedApiModel):
    name: str
    recruiter_profile_url: str
    headline: str
    location: str
    avatar_url: str | None
    viewer_state: RcPersonViewerState


class RcRecruitingActivity(LinkedApiModel):
    projects: int
    messages: int
    feedback: int
    attachments: int


class RcOpenPersonPageParams(BaseActionParams):
    person_url: str
    basic_info: bool | None = None
    recruiting_activity: bool | None = None


class RcOpenPersonPageResult(LinkedApiModel):
    name: str | None = None
    recruiter_profile_url: str | None = None
    headline: str | None = None
    location: str | None = None
    avatar_url: str | None = None
    viewer_state: RcPersonViewerState | None = None
    public_url: str | None = None
    industry: str | None = None
    recruiting_activity: RcRecruitingActivity | None = None
