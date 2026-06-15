from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ActionConfig, ResponseMapping, ThenWorkflowMapper
from linkedapi.types import NvCompany, NvFetchCompanyParams


class NvFetchCompanyMapper(ThenWorkflowMapper[NvFetchCompanyParams, NvCompany]):
    def __init__(self) -> None:
        super().__init__(
            action_configs=[
                ActionConfig(
                    "retrieve_employees",
                    "nv.retrieveCompanyEmployees",
                    "employees_retrieval_config",
                ),
                ActionConfig("retrieve_dms", "nv.retrieveCompanyDMs", "dms_retrieval_config"),
            ],
            response_mappings=[
                ResponseMapping("nv.retrieveCompanyEmployees", "employees"),
                ResponseMapping("nv.retrieveCompanyDMs", "dms"),
            ],
            base_action_type="nv.openCompanyPage",
            default_params={"basicInfo": True},
            result_model=NvCompany,
        )


class NvFetchCompany(Operation[NvFetchCompanyParams, NvCompany]):
    """Fetch a Sales Navigator company page."""

    operation_name = "nvFetchCompany"
    mapper = NvFetchCompanyMapper()
