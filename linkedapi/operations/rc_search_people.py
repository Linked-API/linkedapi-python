from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ArrayWorkflowMapper
from linkedapi.types import RcSearchPeopleParams, RcSearchPeopleResult


class RcSearchPeople(Operation[RcSearchPeopleParams, list[RcSearchPeopleResult]]):
    """Search people on Recruiter Lite.

    Requires a Recruiter Lite seat and the Plus plan (plusPlanRequired otherwise).
    profile_languages accepts LinkedIn language codes such as en, es, in and _o.

    Action errors: filterNotApplied, limitExceeded,
    recruiterSignInRequired, recruiterTwoStepVerificationRequired,
    recruiterMultipleSessionsDetected, unexpectedError.
    See https://linkedapi.io/docs/action-rc-search-people/
    and https://linkedapi.io/docs/recruiter-lite-overview/
    """

    operation_name = "rcSearchPeople"
    mapper = ArrayWorkflowMapper[RcSearchPeopleParams, RcSearchPeopleResult](
        "rc.searchPeople", RcSearchPeopleResult
    )
