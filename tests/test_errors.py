from __future__ import annotations

from linkedapi import (
    LINKED_API_ACTION_ERROR_TYPES,
    LINKED_API_ERROR_TYPES,
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
