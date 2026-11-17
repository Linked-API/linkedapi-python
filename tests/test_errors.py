from __future__ import annotations

from typing import get_args

import pytest
from conftest import FakeHttpClient

from linkedapi import (
    LINKED_API_ACTION_ERROR_TYPES,
    LINKED_API_ERROR_TYPES,
    LinkedApi,
    LinkedApiActionErrorType,
    LinkedApiWorkflowTimeoutError,
)


def test_error_type_sets_match_node_contract() -> None:
    assert LINKED_API_ERROR_TYPES == (
        "linkedApiTokenRequired",
        "invalidLinkedApiToken",
        "identificationTokenRequired",
        "invalidIdentificationToken",
        "subscriptionRequired",
        "trialLimitReached",
        "invalidRequestPayload",
        "invalidWorkflow",
        "plusPlanRequired",
        "linkedinAccountSignedOut",
        "languageNotSupported",
        "workflowTimeout",
        "outsideWorkingHours",
        "workingHoursWaitExpired",
        "cancelledByUser",
        "unexpectedError",
        "httpError",
        "tooManyRequests",
        "accountNotFound",
        "accountIdRequired",
        "sessionNotFound",
        "noAvailableSeats",
        "dailyConnectionAttemptsExceeded",
        "signalLimitReached",
        "signalNotFound",
        "signalStopped",
    )
    assert LINKED_API_ACTION_ERROR_TYPES == (
        "personNotFound",
        "selfProfileNotAllowed",
        "personLikelyChangedPublicUrl",
        "messagingNotAllowed",
        "alreadyPending",
        "alreadyConnected",
        "emailRequired",
        "noteTooLong",
        "noteLimitExceeded",
        "invitationAlreadyReceived",
        "requestNotAllowed",
        "notPending",
        "noPendingRequest",
        "retrievingNotAllowed",
        "connectionNotFound",
        "skillNotFound",
        "endorsementUnavailable",
        "limitExceeded",
        "searchingNotAllowed",
        "searchInterfaceMismatch",
        "searchTemporarilyUnavailable",
        "filterNotApplied",
        "companyNotFound",
        "listNotFound",
        "listAlreadyExists",
        "listNotDeletable",
        "listNotRenamable",
        "savedSearchNotFound",
        "savedSearchAlreadyExists",
        "savedSearchLimitReached",
        "savedSearchRenameUnconfirmed",
        "savedSearchQueryMismatch",
        "postNotFound",
        "jobNotFound",
        "commentingNotAllowed",
        "commentNotFound",
        "replyingNotAllowed",
        "duplicateComment",
        "noPostingPermission",
        "textTooLong",
        "unsupportedAttachmentType",
        "missingDocumentName",
        "urlNotAccessible",
        "fileTooLarge",
        "unsupportedMimeType",
        "tooManyAttachments",
        "mixingNotAllowed",
        "mentionNotResolved",
        "repostNotAllowed",
        "alreadyReposted",
        "recruiterSignInRequired",
        "recruiterTwoStepVerificationRequired",
        "recruiterMultipleSessionsDetected",
        "inMailCreditRequired",
        "inMailNotAvailable",
        "projectNotFound",
        "noSalesNavigator",
        "salesNavigatorOnboardingRequired",
        "conversationsNotSynced",
        "threadNotFound",
        "ssiNotAvailable",
        "unexpectedError",
    )


def test_workflow_timeout_error_fields() -> None:
    error = LinkedApiWorkflowTimeoutError("wf1", "fetchPerson")

    assert error.type == "workflowTimeout"
    assert error.workflow_id == "wf1"
    assert error.operation_name == "fetchPerson"
    assert error.details == {"workflowId": "wf1", "operationName": "fetchPerson"}


@pytest.mark.parametrize(
    "method,action,error_type",
    [
        ("rc_search_people", "rc.searchPeople", "recruiterSignInRequired"),
        ("rc_fetch_person", "rc.openPersonPage", "recruiterTwoStepVerificationRequired"),
        ("rc_sync_inbox", "rc.syncInbox", "recruiterMultipleSessionsDetected"),
        ("rc_send_message", "rc.sendMessage", "inMailCreditRequired"),
        ("rc_send_message", "rc.sendMessage", "inMailNotAvailable"),
        ("rc_save_to_project", "rc.saveToProject", "projectNotFound"),
        ("rc_fetch_person", "rc.openPersonPage", "personNotFound"),
        ("rc_send_message", "rc.sendMessage", "messagingNotAllowed"),
        ("rc_search_people", "rc.searchPeople", "filterNotApplied"),
        ("rc_send_message", "rc.sendMessage", "limitExceeded"),
    ],
)
def test_recruiter_action_errors_keep_type_and_message(
    fake_http_client: FakeHttpClient, method: str, action: str, error_type: str
) -> None:
    op = getattr(LinkedApi(fake_http_client), method)
    message = "Recruiter could not complete this action"
    result = op.mapper.map_response(
        {"actionType": action, "success": False, "error": {"type": error_type, "message": message}}
    )
    assert result.data is None
    assert [(error.type, error.message) for error in result.errors] == [(error_type, message)]
    assert error_type in LINKED_API_ACTION_ERROR_TYPES
    assert error_type in get_args(LinkedApiActionErrorType)
