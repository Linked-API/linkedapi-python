from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import RcSyncInboxParams


class RcSyncInbox(Operation[RcSyncInboxParams, None]):
    """Enable whole-inbox monitoring for Recruiter Lite conversations.

    Requires a Recruiter Lite seat and the Plus plan (plusPlanRequired otherwise).

    Action errors: recruiterSignInRequired,
    recruiterTwoStepVerificationRequired, recruiterMultipleSessionsDetected, unexpectedError.
    See https://linkedapi.io/docs/action-rc-sync-inbox/
    and https://linkedapi.io/docs/recruiter-lite-overview/
    """

    operation_name = "rcSyncInbox"
    mapper = VoidWorkflowMapper[RcSyncInboxParams]("rc.syncInbox")
