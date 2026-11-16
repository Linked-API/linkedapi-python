from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ArrayWorkflowMapper
from linkedapi.types import RcProjectCandidate, RcRetrieveProjectCandidatesParams


class RcRetrieveProjectCandidates(
    Operation[RcRetrieveProjectCandidatesParams, list[RcProjectCandidate]]
):
    """Retrieve candidates from a Recruiter Lite project.

    Requires a Recruiter Lite seat and the Plus plan (plusPlanRequired otherwise).

    Action errors: projectNotFound, recruiterSignInRequired,
    recruiterTwoStepVerificationRequired, recruiterMultipleSessionsDetected, unexpectedError.
    See https://linkedapi.io/docs/action-rc-retrieve-project-candidates/
    and https://linkedapi.io/docs/recruiter-lite-overview/
    """

    operation_name = "rcRetrieveProjectCandidates"
    mapper = ArrayWorkflowMapper[RcRetrieveProjectCandidatesParams, RcProjectCandidate](
        "rc.retrieveProjectCandidates", RcProjectCandidate
    )
