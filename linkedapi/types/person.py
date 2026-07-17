from __future__ import annotations

from typing import Literal, TypeAlias

from linkedapi.types.params import BaseActionParams, LimitSinceParams
from linkedapi.types.post import Comment, Post, Reaction

EmploymentType = Literal[
    "fullTime",
    "partTime",
    "selfEmployed",
    "freelance",
    "contract",
    "internship",
    "apprenticeship",
    "seasonal",
]
LocationType = Literal["onSite", "remote", "hybrid"]
LanguageProficiency = Literal[
    "elementary",
    "limitedWorking",
    "professionalWorking",
    "fullProfessional",
    "nativeOrBilingual",
]
YearsOfExperience = Literal["lessThanOne", "oneToTwo", "threeToFive", "sixToTen", "moreThanTen"]


class BaseFetchPersonParams(BaseActionParams):
    person_url: str
    retrieve_experience: bool | None = None
    retrieve_education: bool | None = None
    retrieve_skills: bool | None = None
    retrieve_languages: bool | None = None
    retrieve_posts: bool | None = None
    retrieve_comments: bool | None = None
    retrieve_reactions: bool | None = None


class BaseFetchPersonParamsWide(BaseFetchPersonParams):
    retrieve_experience: Literal[True] = True
    retrieve_education: Literal[True] = True
    retrieve_skills: Literal[True] = True
    retrieve_languages: Literal[True] = True
    retrieve_posts: Literal[True] = True
    retrieve_comments: Literal[True] = True
    retrieve_reactions: Literal[True] = True


class FetchPersonParams(BaseFetchPersonParams):
    posts_retrieval_config: LimitSinceParams | None = None
    comments_retrieval_config: LimitSinceParams | None = None
    reactions_retrieval_config: LimitSinceParams | None = None


class PersonExperience(BaseActionParams):
    position: str | None = None
    company_name: str | None = None
    company_hashed_url: str | None = None
    employment_type: EmploymentType | None = None
    location_type: LocationType | None = None
    description: str | None = None
    duration: int | None = None
    start_time: str | None = None
    end_time: str | None = None
    location: str | None = None


class PersonEducation(BaseActionParams):
    school_name: str | None = None
    school_hashed_url: str | None = None
    details: str | None = None


class PersonSkill(BaseActionParams):
    name: str | None = None


class PersonLanguage(BaseActionParams):
    name: str | None = None
    proficiency: LanguageProficiency | None = None


class Person(BaseActionParams):
    name: str | None = None
    public_url: str | None = None
    hashed_url: str | None = None
    headline: str | None = None
    location: str | None = None
    country_code: str | None = None
    position: str | None = None
    company_name: str | None = None
    company_hashed_url: str | None = None
    followers_count: int | None = None
    about: str | None = None
    avatar_url: str | None = None
    experiences: list[PersonExperience] | None = None
    education: list[PersonEducation] | None = None
    skills: list[PersonSkill] | None = None
    languages: list[PersonLanguage] | None = None
    posts: list[Post] | None = None
    comments: list[Comment] | None = None
    reactions: list[Reaction] | None = None


FetchPersonResult: TypeAlias = Person
