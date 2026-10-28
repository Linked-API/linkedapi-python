from __future__ import annotations

from typing import Any, Literal

LinkedApiActionErrorType = Literal[
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
]
LINKED_API_ACTION_ERROR_TYPES: tuple[str, ...] = (
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

LinkedApiErrorType = Literal[
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
]
LINKED_API_ERROR_TYPES: tuple[str, ...] = (
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


class LinkedApiError(Exception):
    type: str
    message: str
    details: Any | None

    def __init__(self, type: str, message: str, details: Any | None = None) -> None:
        super().__init__(message)
        self.type = type
        self.message = message
        self.details = details

    @classmethod
    def unknown_error(
        cls, message: str = "Unknown error. Please contact support."
    ) -> LinkedApiError:
        return cls("unknownError", message)


class LinkedApiWorkflowTimeoutError(LinkedApiError):
    workflow_id: str
    operation_name: str

    def __init__(self, workflow_id: str, operation_name: str) -> None:
        message = (
            f"Workflow {workflow_id} timed out. Call {operation_name}.result() again to continue "
            "checking the workflow."
        )
        super().__init__(
            "workflowTimeout",
            message,
            {"workflowId": workflow_id, "operationName": operation_name},
        )
        self.workflow_id = workflow_id
        self.operation_name = operation_name
