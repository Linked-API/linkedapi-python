from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import RcRenameProjectParams


class RcRenameProject(Operation[RcRenameProjectParams, None]):
    """Rename a Recruiter Lite project and optionally update its description.

    Requires a Recruiter Lite seat and the Plus plan (plusPlanRequired otherwise).

    Action errors: projectNotFound, recruiterSignInRequired,
    recruiterTwoStepVerificationRequired, recruiterMultipleSessionsDetected, unexpectedError.
    See https://linkedapi.io/docs/action-rc-rename-project/
    and https://linkedapi.io/docs/recruiter-lite-overview/
    """

    operation_name = "rcRenameProject"
    mapper = VoidWorkflowMapper[RcRenameProjectParams]("rc.renameProject")
