from __future__ import annotations

from typing import Literal

from pydantic import model_validator

from linkedapi.types.base import LinkedApiModel
from linkedapi.types.params import BaseActionParams, LimitParams

ConnectionStatus = Literal["connected", "pending", "incoming", "notConnected"]
InvitationType = Literal["connect", "companyFollow", "newsletterSubscribe"]


class ConnectionPerson(LinkedApiModel):
    name: str | None = None
    public_url: str | None = None
    headline: str | None = None
    location: str | None = None
    profile_image_url: str | None = None


class SendConnectionRequestParams(BaseActionParams):
    person_url: str
    note: str | None = None
    email: str | None = None


class CheckConnectionStatusParams(BaseActionParams):
    person_url: str


class CheckConnectionStatusResult(LinkedApiModel):
    connection_status: ConnectionStatus | None = None


class WithdrawConnectionRequestParams(BaseActionParams):
    person_url: str
    unfollow: bool | None = None


class RetrievePendingRequestsResult(LinkedApiModel):
    name: str | None = None
    public_url: str | None = None
    headline: str | None = None
    sent_time: str | None = None


class InvitationTargetParams(BaseActionParams):
    invitation_type: InvitationType
    person_url: str | None = None
    company_url: str | None = None
    newsletter_url: str | None = None

    @model_validator(mode="after")
    def validate_target_url(self) -> InvitationTargetParams:
        target_urls = {
            "connect": self.person_url,
            "companyFollow": self.company_url,
            "newsletterSubscribe": self.newsletter_url,
        }
        if target_urls[self.invitation_type] is None:
            msg = f"{self.invitation_type} invitation requires its matching target URL"
            raise ValueError(msg)
        if sum(url is not None for url in target_urls.values()) != 1:
            msg = "Provide only the target URL that matches invitation_type"
            raise ValueError(msg)
        return self


class AcceptInvitationParams(InvitationTargetParams):
    pass


class IgnoreInvitationParams(InvitationTargetParams):
    pass


class Invitation(LinkedApiModel):
    invitation_type: InvitationType
    name: str
    public_url: str
    headline: str | None = None
    note: str | None = None
    company_url: str | None = None
    company_name: str | None = None
    newsletter_url: str | None = None
    newsletter_name: str | None = None

    @model_validator(mode="after")
    def validate_type_fields(self) -> Invitation:
        type_fields = {
            "headline",
            "note",
            "company_url",
            "company_name",
            "newsletter_url",
            "newsletter_name",
        }
        required_fields = {
            "connect": {"headline", "note"},
            "companyFollow": {"company_url", "company_name"},
            "newsletterSubscribe": {"newsletter_url", "newsletter_name"},
        }[self.invitation_type]
        missing_fields = required_fields - self.model_fields_set
        if missing_fields:
            msg = (
                f"{self.invitation_type} invitation is missing required fields: "
                f"{', '.join(sorted(missing_fields))}"
            )
            raise ValueError(msg)

        unexpected_fields = (self.model_fields_set & type_fields) - required_fields
        if unexpected_fields:
            msg = (
                f"{self.invitation_type} invitation contains fields for another type: "
                f"{', '.join(sorted(unexpected_fields))}"
            )
            raise ValueError(msg)

        target_url = {
            "connect": self.public_url,
            "companyFollow": self.company_url,
            "newsletterSubscribe": self.newsletter_url,
        }[self.invitation_type]
        if target_url is None:
            msg = f"{self.invitation_type} invitation requires a non-null target URL"
            raise ValueError(msg)
        return self


class RetrieveConnectionsFilter(LinkedApiModel):
    first_name: str | None = None
    last_name: str | None = None
    position: str | None = None
    locations: list[str] | None = None
    industries: list[str] | None = None
    current_companies: list[str] | None = None
    previous_companies: list[str] | None = None
    schools: list[str] | None = None


class RetrieveConnectionsParams(LimitParams):
    since: str | None = None
    filter: RetrieveConnectionsFilter | None = None


class RetrieveConnectionsResult(LinkedApiModel):
    name: str | None = None
    public_url: str | None = None
    headline: str | None = None
    location: str | None = None
    connected_at: str | None = None


class RemoveConnectionParams(BaseActionParams):
    person_url: str


class NvOpenPersonPageParams(BaseActionParams):
    person_hashed_url: str


class NvOpenPersonPageResult(LinkedApiModel):
    name: str | None = None
    public_url: str | None = None
    hashed_url: str | None = None
    headline: str | None = None
    location: str | None = None
    country_code: str | None = None
    position: str | None = None
    company_name: str | None = None
    company_hashed_url: str | None = None
