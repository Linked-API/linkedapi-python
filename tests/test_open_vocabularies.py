from __future__ import annotations

import json
from types import UnionType
from typing import Any, Literal, Union, get_args, get_origin

import pytest
from pydantic import ValidationError

import linkedapi as sdk
from linkedapi.types.base import LinkedApiModel

FUTURE_VALUE = "someFutureValue"
PERSON_URL = "https://www.linkedin.com/in/fixture-person"

RESPONSE_VOCABULARIES = [
    ("AccountWebhookEvent", "type", "account.active"),
    ("AccountWebhookEventData", "status", "active"),
    ("AdminAccount", "status", "active"),
    ("CheckConnectionStatusResult", "connection_status", "connected"),
    ("ConnectionSession", "status", "pending"),
    ("ContentViewerState", "reaction", "like"),
    ("ConversationPollResult", "type", "st"),
    ("FeedPost", "type", "original"),
    ("InboxMessage", "type", "st"),
    ("InboxMessage", "sender", "us"),
    ("InboxPersonMessage", "type", "st"),
    ("InboxPersonMessage", "sender", "us"),
    ("InboxPersonThread", "type", "st"),
    ("Invitation", "invitation_type", "connect"),
    ("JobSalary", "currency", "usd"),
    ("JobSalary", "period", "yearly"),
    ("Limit", "category", "stPersonProfileViews"),
    ("Limit", "period", "daily"),
    ("LimitUsage", "category", "stPersonProfileViews"),
    ("LimitUsage", "period", "daily"),
    ("LinkedApiActionError", "type", "personNotFound"),
    ("Message", "sender", "us"),
    ("MessageWebhookEvent", "type", "inbox.messageReceived"),
    ("MessageWebhookEventData", "type", "st"),
    ("MessageWebhookEventData", "sender", "us"),
    ("NetworkEvent", "type", "connectionAccepted"),
    ("NetworkWebhookEvent", "type", "network.connectionAccepted"),
    ("PersonExperience", "employment_type", "fullTime"),
    ("PersonExperience", "location_type", "onSite"),
    ("PersonLanguage", "proficiency", "elementary"),
    ("PersonViewerState", "connection_degree", "1st"),
    ("Post", "type", "original"),
    ("PostAuthor", "type", "person"),
    ("PostComment", "commenter_type", "person"),
    ("PostCommentAuthor", "type", "person"),
    ("PostReaction", "engager_type", "person"),
    ("PostReaction", "type", "like"),
    ("PostReposter", "type", "person"),
    ("ProfileViewer", "viewer_type", "identified"),
    ("ProfileViewer", "connection_degree", 1),
    ("Reaction", "reaction_type", "like"),
    ("SearchPostActor", "type", "person"),
    ("SearchPostResult", "type", "original"),
    ("SetSeatsResult", "status", "complete"),
    ("SubscriptionSeat", "seat_type", "core"),
    ("SubscriptionSeat", "billing_period", "month"),
    ("SubscriptionStatus", "status", "active"),
    ("WebhookDelivery", "status", "pending"),
    ("WebhookSubscription", "payload_mode", "thin"),
    ("WebhookTestEvent", "type", "webhook.test"),
    ("WorkflowInProgressResponse", "workflow_status", "pending"),
    ("WorkflowInProgressResponse", "pending_reason", "queued"),
    ("WorkflowResponse", "workflow_status", "pending"),
    ("WorkflowResponse", "pending_reason", "queued"),
    ("WorkflowStartedResponse", "workflow_status", "pending"),
    ("WorkflowStartedResponse", "pending_reason", "queued"),
    ("WorkflowWebhookEvent", "type", "workflow.created"),
    ("WorkflowWebhookEventData", "status", "pending"),
]

REQUEST_VOCABULARIES = [
    ("AcceptInvitationParams", "invitation_type", "connect", False),
    ("AnnualRevenueFilter", "min", "0", False),
    ("AnnualRevenueFilter", "max", "0.5", False),
    ("ConversationPollRequest", "type", "st", False),
    ("CreatePostAttachment", "type", "image", False),
    ("DeleteLimitEntry", "category", "stPersonProfileViews", False),
    ("DeleteLimitEntry", "period", "daily", False),
    ("IgnoreInvitationParams", "invitation_type", "connect", False),
    ("InboxPersonPollRequest", "type", "st", False),
    ("InboxPollRequest", "type", "st", False),
    ("InvitationTargetParams", "invitation_type", "connect", False),
    ("NetworkPollRequest", "type", "connectionAccepted", False),
    ("NvCompanyEmployeeFilter", "years_of_experiences", "lessThanOne", True),
    ("NvCompanyEmployeeFilter", "connection_degrees", "1st", True),
    ("NvSearchCompaniesFilter", "sizes", "1-10", True),
    ("NvSearchPeopleFilter", "connection_degrees", "1st", True),
    ("NvSearchPeopleFilter", "years_of_experiences", "lessThanOne", True),
    ("PostCommentsRetrievalConfig", "sort", "mostRelevant", False),
    ("ReactToCommentParams", "type", "like", False),
    ("ReactToPostParams", "type", "like", False),
    ("SearchCompaniesFilter", "sizes", "1-10", True),
    ("SearchJobsFilter", "date_posted", "anyTime", False),
    ("SearchJobsFilter", "experience_levels", "internship", True),
    ("SearchJobsFilter", "employment_types", "fullTime", True),
    ("SearchJobsFilter", "workplace_types", "onSite", True),
    ("SearchJobsPreferences", "date_posted", "anyTime", False),
    ("SearchJobsPreferences", "experience_levels", "entryLevel", True),
    ("SearchJobsPreferences", "employment_types", "fullTime", True),
    ("SearchPeopleFilter", "connection_degrees", "1st", True),
    ("SearchPostsFilter", "sort", "topMatch", False),
    ("SearchPostsFilter", "date_posted", "past24Hours", False),
    ("SearchPostsFilter", "content_type", "videos", False),
    ("SearchPostsFilter", "posted_by", "me", True),
    ("SetLimitEntry", "category", "stPersonProfileViews", False),
    ("SetLimitEntry", "period", "daily", False),
    ("SetSeatsParams", "seat_type", "core", False),
    ("SetSeatsParams", "billing_period", "month", False),
    ("SetWebhookEventsParams", "events", "workflow.created", True),
    ("SetWebhookParams", "payload_mode", "thin", False),
    ("SetWebhookParams", "events", "workflow.created", True),
    ("SetWebhookPayloadModeParams", "payload_mode", "thin", False),
    ("StCompanyEmployeesFilter", "connection_degrees", "1st", True),
]


VALID_PAYLOADS: dict[str, dict[str, Any]] = {
    "AnnualRevenueFilter": {"min": "0", "max": "0.5"},
    "Invitation": {"name": "Fixture Person", "publicUrl": PERSON_URL},
    "LinkedApiActionError": {"message": "Fixture error"},
    "ConversationPollRequest": {"personUrl": PERSON_URL, "type": "st"},
    "InboxPersonPollRequest": {"personUrl": PERSON_URL},
    "InvitationTargetParams": {"invitationType": "connect", "personUrl": PERSON_URL},
    "AcceptInvitationParams": {"invitationType": "connect", "personUrl": PERSON_URL},
    "IgnoreInvitationParams": {"invitationType": "connect", "personUrl": PERSON_URL},
    "CreatePostAttachment": {"url": "https://example.test/image.png", "type": "image"},
    "ReactToPostParams": {
        "postUrl": "https://www.linkedin.com/feed/update/fixture",
        "type": "like",
    },
    "ReactToCommentParams": {"commentUrl": "https://www.linkedin.com/feed/update/fixture"},
    "SetLimitEntry": {"category": "stMessages", "period": "daily", "maxValue": 50},
    "DeleteLimitEntry": {"category": "stMessages", "period": "daily"},
    "SetSeatsParams": {"quantity": 1, "seatType": "core", "billingPeriod": "month"},
    "SetWebhookParams": {"url": "https://example.test/webhook"},
    "SetWebhookPayloadModeParams": {"id": "webhook-1", "payloadMode": "thin"},
    "SetWebhookEventsParams": {"id": "webhook-1", "events": ["workflow.created"]},
}


def model_class(name: str) -> type[LinkedApiModel]:
    return getattr(sdk, name)


def valid_payload(model_name: str) -> dict[str, Any]:
    if model_name in {"WorkflowStartedResponse", "WorkflowInProgressResponse", "WorkflowResponse"}:
        return {"workflowId": "workflow-1", "workflowStatus": "pending"}
    if model_name.endswith("WebhookEvent") or model_name == "WebhookTestEvent":
        return {"id": "event-1", "data": {}}
    if model_name == "ProfileViewer":
        return {
            "viewerType": "identified",
            "viewedAt": None,
            "viewedAgo": None,
            "name": "Fixture Person",
            "publicUrl": PERSON_URL,
            "urn": None,
            "headline": None,
            "connectionDegree": 1,
            "avatarUrl": None,
        }
    return dict(VALID_PAYLOADS.get(model_name, {}))


@pytest.mark.parametrize("model_name, field_name, known", RESPONSE_VOCABULARIES)
@pytest.mark.parametrize("value_kind", ["known", "future"])
def test_response_vocabularies_keep_known_and_future_values(
    model_name: str, field_name: str, known: str | int, value_kind: str
) -> None:
    model = model_class(model_name)
    payload = valid_payload(model_name)
    value = known if value_kind == "known" else 4 if isinstance(known, int) else FUTURE_VALUE
    if model_name == "Invitation" and value_kind == "known":
        payload.update({"headline": None, "note": None})
    if model_name == "ProfileViewer" and field_name == "viewer_type" and value_kind == "future":
        payload = {"viewedAt": None, "viewedAgo": None}
    alias = model.model_fields[field_name].alias or field_name
    payload[alias] = value

    parsed = model.model_validate(payload)

    assert getattr(parsed, field_name) == value
    assert type(getattr(parsed, field_name)) is type(value)
    assert parsed.model_dump(by_alias=True)[alias] == value


@pytest.mark.parametrize("viewer_type", ["identified", "anonymous"])
def test_known_profile_viewer_types_still_require_their_fields(viewer_type: str) -> None:
    with pytest.raises(ValidationError):
        sdk.ProfileViewer.model_validate(
            {"viewerType": viewer_type, "viewedAt": None, "viewedAgo": None}
        )


@pytest.mark.parametrize("model_name, field_name, known, is_list", REQUEST_VOCABULARIES)
def test_request_vocabularies_keep_rejecting_unknown_values(
    model_name: str, field_name: str, known: str, is_list: bool
) -> None:
    model = model_class(model_name)
    alias = model.model_fields[field_name].alias or field_name
    payload = valid_payload(model_name)
    payload[alias] = [known] if is_list else known
    parsed = model.model_validate(payload)
    assert getattr(parsed, field_name) == payload[alias]

    payload[alias] = [FUTURE_VALUE] if is_list else FUTURE_VALUE
    with pytest.raises(ValidationError) as error:
        model.model_validate(payload)

    assert any(item["loc"][0] in (alias, field_name) for item in error.value.errors())


def referenced_models(annotation: Any) -> set[type[LinkedApiModel]]:
    if isinstance(annotation, type) and issubclass(annotation, LinkedApiModel):
        return {annotation}
    return {model for argument in get_args(annotation) for model in referenced_models(argument)}


def reachable_models(roots: set[type[LinkedApiModel]]) -> set[type[LinkedApiModel]]:
    models = set(roots)
    pending = list(roots)
    while pending:
        model = pending.pop()
        for field in model.model_fields.values():
            for child in referenced_models(field.annotation) - models:
                models.add(child)
                pending.append(child)
    return models


def response_models() -> set[type[LinkedApiModel]]:
    exported = {
        value
        for value in vars(sdk).values()
        if isinstance(value, type) and issubclass(value, LinkedApiModel)
    }
    request_roots = {
        model
        for model in exported
        if model.__name__.endswith(("Params", "ParamsWide", "Request"))
        or model.__name__ == "AdminConfig"
    }
    requests = reachable_models(request_roots)
    established_responses = {model_class(name) for name, _, _ in RESPONSE_VOCABULARIES}
    # A response model reused by a request still follows the open-response contract.
    return reachable_models((exported - requests) | established_responses)


def closed_vocabulary(annotation: Any) -> bool:
    origin = get_origin(annotation)
    arguments = get_args(annotation)
    if origin is Literal:
        return any(
            isinstance(value, (str, int)) and not isinstance(value, bool) for value in arguments
        )
    if origin in (Union, UnionType):
        for argument in arguments:
            if get_origin(argument) is Literal:
                values = [value for value in get_args(argument) if not isinstance(value, bool)]
                if values and all(type(value) in arguments for value in values):
                    continue
            if closed_vocabulary(argument):
                return True
        return False
    return any(closed_vocabulary(argument) for argument in arguments)


def literal_values(annotation: Any) -> list[Any]:
    if get_origin(annotation) is Literal:
        return list(get_args(annotation))
    return [value for argument in get_args(annotation) for value in literal_values(argument)]


def test_response_models_do_not_gain_closed_literal_vocabularies() -> None:
    closed = sorted(
        f"{model.__name__}.{name}"
        for model in response_models()
        for name, field in model.model_fields.items()
        if closed_vocabulary(field.annotation)
    )

    assert closed == []


def test_known_response_literal_hints_are_preserved() -> None:
    missing = [
        f"{name}.{field_name}"
        for name, field_name, known in RESPONSE_VOCABULARIES
        if known not in literal_values(model_class(name).model_fields[field_name].annotation)
    ]

    assert missing == []


@pytest.mark.parametrize("event_type", ["future.newEvent", "workflow.someFutureType"])
def test_unknown_webhook_types_keep_the_common_envelope_and_raw_payload(event_type: str) -> None:
    payload = {
        "id": "future-event-1",
        "type": event_type,
        "createdAt": "2026-10-15T12:00:00Z",
        "data": {"newField": {"phase": FUTURE_VALUE}, "items": [1, "two"]},
    }

    event = sdk.parse_webhook_event(json.dumps(payload).encode())

    assert isinstance(event, sdk.UnknownWebhookEvent)
    assert event.id == payload["id"]
    assert event.type == event_type
    assert event.created_at == payload["createdAt"]
    assert event.data == payload["data"]


def test_known_webhook_type_still_returns_the_specific_model() -> None:
    event = sdk.parse_webhook_event(
        json.dumps(
            {
                "id": "known-event-1",
                "type": "workflow.completed",
                "data": {"workflowId": "workflow-1", "status": "completed"},
            }
        )
    )

    assert isinstance(event, sdk.WorkflowWebhookEvent)
    assert event.type == "workflow.completed"
    assert event.data.workflow_id == "workflow-1"
    assert event.data.status == "completed"


@pytest.mark.parametrize(
    "raw_body",
    [
        "not JSON",
        "[]",
        json.dumps({"type": "workflow.completed", "data": {}}),
        json.dumps({"id": "event-1", "data": {}}),
        json.dumps({"id": 42, "type": "workflow.completed", "data": {}}),
        json.dumps({"id": "event-1", "type": 42, "data": {}}),
        json.dumps({"id": "event-1", "type": "workflow.completed", "data": "invalid"}),
        json.dumps({"id": "event-1", "type": "future.newEvent", "data": "invalid"}),
    ],
)
def test_malformed_webhook_envelopes_still_raise(raw_body: str) -> None:
    with pytest.raises(ValueError):
        sdk.parse_webhook_event(raw_body)
