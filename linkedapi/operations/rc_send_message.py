from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import SimpleWorkflowMapper
from linkedapi.types import RcSendMessageParams, RcSendMessageResult


class RcSendMessage(Operation[RcSendMessageParams, RcSendMessageResult]):
    """Send a Recruiter Lite InMail or reply to a thread.

    Requires a Recruiter Lite seat and the Plus plan (plusPlanRequired otherwise).
    Use person_url + subject + text for a new InMail, or thread_id + text for a reply.
    Paid credits require allow_paid_credit=True; the default is free messages only.
    After an unexpectedError, check Messages before resending: the send may have succeeded.

    Action errors: personNotFound, messagingNotAllowed, inMailCreditRequired,
    inMailNotAvailable, limitExceeded, recruiterSignInRequired,
    recruiterTwoStepVerificationRequired, recruiterMultipleSessionsDetected, unexpectedError.
    See https://linkedapi.io/docs/action-rc-send-message/
    and https://linkedapi.io/docs/recruiter-lite-overview/
    """

    operation_name = "rcSendMessage"
    mapper = SimpleWorkflowMapper[RcSendMessageParams, RcSendMessageResult](
        "rc.sendMessage", result_model=RcSendMessageResult
    )
