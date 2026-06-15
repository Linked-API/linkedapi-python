from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ActionConfig, ResponseMapping, ThenWorkflowMapper
from linkedapi.types import Company, FetchCompanyParams


class FetchCompanyMapper(ThenWorkflowMapper[FetchCompanyParams, Company]):
    def __init__(self) -> None:
        super().__init__(
            action_configs=[
                ActionConfig(
                    "retrieve_employees",
                    "st.retrieveCompanyEmployees",
                    "employees_retrieval_config",
                ),
                ActionConfig("retrieve_dms", "st.retrieveCompanyDMs", "dms_retrieval_config"),
                ActionConfig("retrieve_posts", "st.retrieveCompanyPosts", "posts_retrieval_config"),
            ],
            response_mappings=[
                ResponseMapping("st.retrieveCompanyEmployees", "employees"),
                ResponseMapping("st.retrieveCompanyDMs", "dms"),
                ResponseMapping("st.retrieveCompanyPosts", "posts"),
            ],
            base_action_type="st.openCompanyPage",
            default_params={"basicInfo": True},
            result_model=Company,
        )


class FetchCompany(Operation[FetchCompanyParams, Company]):
    """Fetch a standard LinkedIn company page."""

    operation_name = "fetchCompany"
    mapper = FetchCompanyMapper()
