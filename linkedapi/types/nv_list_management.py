from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field, StringConstraints

from linkedapi.types.base import LinkedApiModel
from linkedapi.types.params import BaseActionParams


class NvCreateListParams(BaseActionParams):
    type: Literal["lead", "account"]
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=75)]
    description: str | None = Field(default=None, max_length=350)


class NvDeleteListParams(BaseActionParams):
    list_id: str = Field(min_length=1)


class NvCreatedList(LinkedApiModel):
    id: str
    name: str
    type: Literal["lead", "account"] | str
    url: str


class NvRenameListParams(BaseActionParams):
    list_id: str = Field(min_length=1)
    name: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True, min_length=1, max_length=75, pattern=r"^[^\r\n]+$"
        ),
    ]
