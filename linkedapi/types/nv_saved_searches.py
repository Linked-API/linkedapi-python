from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field, StringConstraints

from linkedapi.types.base import LinkedApiModel
from linkedapi.types.params import BaseActionParams


class NvRetrieveSavedSearchesParams(BaseActionParams):
    type: Literal["lead", "account"]


class NvCreateSavedSearchParams(BaseActionParams):
    type: Literal["lead", "account"]
    custom_search_url: str = Field(min_length=1)
    name: (
        Annotated[
            str,
            StringConstraints(
                strip_whitespace=True,
                min_length=1,
                max_length=256,
                pattern=r"^[^\r\n\u2028\u2029]+$",
            ),
        ]
        | None
    ) = None


class NvDeleteSavedSearchParams(BaseActionParams):
    saved_search_id: str = Field(pattern=r"^[1-9]\d*$")


class NvCreatedSavedSearch(LinkedApiModel):
    id: str
    name: str
    type: Literal["lead", "account"] | str
    url: str


class NvSavedSearch(LinkedApiModel):
    id: str
    name: str
    type: Literal["lead", "account"] | str
    url: str
    keywords: str | None
    created_at: str | None
    last_viewed_at: str | None
    new_results_count: int | None
