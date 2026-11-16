from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ThenWorkflowMapper
from linkedapi.types import RcOpenPersonPageParams, RcOpenPersonPageResult


class RcFetchPersonMapper(ThenWorkflowMapper[RcOpenPersonPageParams, RcOpenPersonPageResult]):
    def __init__(self) -> None:
        super().__init__(
            action_configs=[],
            response_mappings=[],
            base_action_type="rc.openPersonPage",
            default_params={"basicInfo": True},
            result_model=RcOpenPersonPageResult,
        )


class RcFetchPerson(Operation[RcOpenPersonPageParams, RcOpenPersonPageResult]):
    """Fetch a Recruiter Lite profile, optionally including recruiting activity.

    Requires a Recruiter Lite seat and the Plus plan (plusPlanRequired otherwise).
    basic_info defaults to True; recruiting_activity requests the seat's activity counts.
    person_url must be a Recruiter profile URL (https://www.linkedin.com/talent/profile/...).

    Action errors: personNotFound, limitExceeded, recruiterSignInRequired,
    recruiterTwoStepVerificationRequired, recruiterMultipleSessionsDetected, unexpectedError.
    See https://linkedapi.io/docs/action-rc-open-person-page/
    and https://linkedapi.io/docs/recruiter-lite-overview/
    """

    operation_name = "rcFetchPerson"
    mapper = RcFetchPersonMapper()
