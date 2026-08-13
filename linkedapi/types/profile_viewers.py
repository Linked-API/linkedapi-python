from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from linkedapi.types.base import LinkedApiModel
from linkedapi.types.params import BaseActionParams

ProfileViewerType = Literal["identified", "anonymous"]


class RetrieveProfileViewersParams(BaseActionParams):
    limit: int | None = Field(default=None, ge=1, le=300)
    since: str | None = None


class ProfileViewer(LinkedApiModel):
    viewer_type: ProfileViewerType
    viewed_at: str | None
    viewed_ago: str | None
    name: str | None = None
    public_url: str | None = None
    urn: str | None = None
    headline: str | None = None
    connection_degree: Literal[1, 2, 3] | None = None
    avatar_url: str | None = None
    description: str | None = None
    search_url: str | None = None

    @model_validator(mode="after")
    def validate_type_fields(self) -> ProfileViewer:
        type_fields = {
            "name",
            "public_url",
            "urn",
            "headline",
            "connection_degree",
            "avatar_url",
            "description",
            "search_url",
        }
        required_fields = {
            "identified": {
                "name",
                "public_url",
                "urn",
                "headline",
                "connection_degree",
                "avatar_url",
            },
            "anonymous": {"description", "search_url"},
        }[self.viewer_type]
        missing_fields = required_fields - self.model_fields_set
        if missing_fields:
            msg = (
                f"{self.viewer_type} profile viewer is missing required fields: "
                f"{', '.join(sorted(missing_fields))}"
            )
            raise ValueError(msg)

        unexpected_fields = (self.model_fields_set & type_fields) - required_fields
        if unexpected_fields:
            msg = (
                f"{self.viewer_type} profile viewer contains fields for another type: "
                f"{', '.join(sorted(unexpected_fields))}"
            )
            raise ValueError(msg)

        required_values = {
            "identified": {"name": self.name, "public_url": self.public_url},
            "anonymous": {"description": self.description, "search_url": self.search_url},
        }[self.viewer_type]
        null_fields = [name for name, value in required_values.items() if value is None]
        if null_fields:
            msg = (
                f"{self.viewer_type} profile viewer requires non-null fields: "
                f"{', '.join(sorted(null_fields))}"
            )
            raise ValueError(msg)

        return self
