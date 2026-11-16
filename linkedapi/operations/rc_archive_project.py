from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import SimpleWorkflowMapper
from linkedapi.types import RcArchiveProjectParams, RcArchiveProjectResult


class RcArchiveProject(Operation[RcArchiveProjectParams, RcArchiveProjectResult]):
    """Archive a Recruiter Lite project.

    Requires a Recruiter Lite seat and the Plus plan (plusPlanRequired otherwise).

    Action errors: projectNotFound, recruiterSignInRequired,
    recruiterTwoStepVerificationRequired, recruiterMultipleSessionsDetected, unexpectedError.
    See https://linkedapi.io/docs/action-rc-archive-project/
    and https://linkedapi.io/docs/recruiter-lite-overview/
    """

    operation_name = "rcArchiveProject"
    mapper = SimpleWorkflowMapper[RcArchiveProjectParams, RcArchiveProjectResult](
        "rc.archiveProject", result_model=RcArchiveProjectResult
    )
