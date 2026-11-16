from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import SimpleWorkflowMapper
from linkedapi.types import RcCreatedProject, RcCreateProjectParams


class RcCreateProject(Operation[RcCreateProjectParams, RcCreatedProject]):
    """Create a private Recruiter Lite project by name.

    Requires a Recruiter Lite seat and the Plus plan (plusPlanRequired otherwise).
    After a failure, check existing projects before creating again: creation may have succeeded.

    Action errors: recruiterSignInRequired,
    recruiterTwoStepVerificationRequired, recruiterMultipleSessionsDetected, unexpectedError.
    See https://linkedapi.io/docs/action-rc-create-project/
    and https://linkedapi.io/docs/recruiter-lite-overview/
    """

    operation_name = "rcCreateProject"
    mapper = SimpleWorkflowMapper[RcCreateProjectParams, RcCreatedProject](
        "rc.createProject", result_model=RcCreatedProject
    )
