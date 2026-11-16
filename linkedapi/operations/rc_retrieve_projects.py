from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ArrayWorkflowMapper
from linkedapi.types import RcProject, RcRetrieveProjectsParams


class RcRetrieveProjects(Operation[RcRetrieveProjectsParams, list[RcProject]]):
    """Retrieve Recruiter Lite projects.

    Requires a Recruiter Lite seat and the Plus plan (plusPlanRequired otherwise).

    Action errors: recruiterSignInRequired,
    recruiterTwoStepVerificationRequired, recruiterMultipleSessionsDetected, unexpectedError.
    See https://linkedapi.io/docs/action-rc-retrieve-projects/
    and https://linkedapi.io/docs/recruiter-lite-overview/
    """

    operation_name = "rcRetrieveProjects"
    mapper = ArrayWorkflowMapper[RcRetrieveProjectsParams, RcProject](
        "rc.retrieveProjects", RcProject
    )
