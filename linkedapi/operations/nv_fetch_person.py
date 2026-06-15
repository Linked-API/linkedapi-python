from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ThenWorkflowMapper
from linkedapi.types import NvOpenPersonPageParams, NvOpenPersonPageResult


class NvFetchPersonMapper(ThenWorkflowMapper[NvOpenPersonPageParams, NvOpenPersonPageResult]):
    def __init__(self) -> None:
        super().__init__(
            action_configs=[],
            response_mappings=[],
            base_action_type="nv.openPersonPage",
            default_params={"basicInfo": True},
            result_model=NvOpenPersonPageResult,
        )


class NvFetchPerson(Operation[NvOpenPersonPageParams, NvOpenPersonPageResult]):
    """Fetch a Sales Navigator person profile."""

    operation_name = "nvFetchPerson"
    mapper = NvFetchPersonMapper()
