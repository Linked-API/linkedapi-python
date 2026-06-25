from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ThenWorkflowMapper
from linkedapi.types import FetchJobParams, Job


class FetchJobMapper(ThenWorkflowMapper[FetchJobParams, Job]):
    def __init__(self) -> None:
        super().__init__(
            action_configs=[],
            response_mappings=[],
            base_action_type="st.openJob",
            default_params={"basicInfo": True},
            result_model=Job,
        )


class FetchJob(Operation[FetchJobParams, Job]):
    """Fetch a LinkedIn job."""

    operation_name = "fetchJob"
    mapper = FetchJobMapper()
