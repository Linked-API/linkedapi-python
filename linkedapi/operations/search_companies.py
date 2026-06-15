from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ArrayWorkflowMapper
from linkedapi.types import SearchCompaniesParams, SearchCompanyResult


class SearchCompanies(Operation[SearchCompaniesParams, list[SearchCompanyResult]]):
    """Search companies on standard LinkedIn."""

    operation_name = "searchCompanies"
    mapper = ArrayWorkflowMapper[SearchCompaniesParams, SearchCompanyResult](
        "st.searchCompanies",
        SearchCompanyResult,
    )
