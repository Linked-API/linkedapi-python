from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import SimpleWorkflowMapper
from linkedapi.types import RcSaveToProjectParams, RcSaveToProjectResult


class RcSaveToProject(Operation[RcSaveToProjectParams, RcSaveToProjectResult]):
    """Save a Recruiter Lite candidate to a project.

    Requires a Recruiter Lite seat and the Plus plan (plusPlanRequired otherwise).

    Action errors: projectNotFound, limitExceeded,
    recruiterSignInRequired, recruiterTwoStepVerificationRequired,
    recruiterMultipleSessionsDetected, unexpectedError.
    See https://linkedapi.io/docs/action-rc-save-to-project/
    and https://linkedapi.io/docs/recruiter-lite-overview/
    """

    operation_name = "rcSaveToProject"
    mapper = SimpleWorkflowMapper[RcSaveToProjectParams, RcSaveToProjectResult](
        "rc.saveToProject", result_model=RcSaveToProjectResult
    )
