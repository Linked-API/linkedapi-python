from __future__ import annotations

from typing import Any, Literal

LinkedApiActionErrorType = Literal[
    "personNotFound",
    "selfProfileNotAllowed",
    "messagingNotAllowed",
    "alreadyPending",
    "alreadyConnected",
    "emailRequired",
    "noteTooLong",
    "noteLimitExceeded",
    "requestNotAllowed",
    "notPending",
    "retrievingNotAllowed",
    "connectionNotFound",
    "searchingNotAllowed",
    "companyNotFound",
    "postNotFound",
    "jobNotFound",
    "commentingNotAllowed",
    "noPostingPermission",
    "noSalesNavigator",
    "conversationsNotSynced",
    "threadNotFound",
]
LINKED_API_ACTION_ERROR_TYPES: tuple[str, ...] = (
    "personNotFound",
    "selfProfileNotAllowed",
    "messagingNotAllowed",
    "alreadyPending",
    "alreadyConnected",
    "emailRequired",
    "noteTooLong",
    "noteLimitExceeded",
    "requestNotAllowed",
    "notPending",
    "retrievingNotAllowed",
    "connectionNotFound",
    "searchingNotAllowed",
    "companyNotFound",
    "postNotFound",
    "jobNotFound",
    "commentingNotAllowed",
    "noPostingPermission",
    "noSalesNavigator",
    "conversationsNotSynced",
    "threadNotFound",
)

LinkedApiErrorType = Literal[
    "linkedApiTokenRequired",
    "invalidLinkedApiToken",
    "identificationTokenRequired",
    "invalidIdentificationToken",
    "subscriptionRequired",
    "invalidRequestPayload",
    "invalidWorkflow",
    "plusPlanRequired",
    "linkedinAccountSignedOut",
    "languageNotSupported",
    "workflowTimeout",
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
    "invalidRequestPayload",
    "invalidWorkflow",
    "plusPlanRequired",
    "linkedinAccountSignedOut",
    "languageNotSupported",
    "workflowTimeout",
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
