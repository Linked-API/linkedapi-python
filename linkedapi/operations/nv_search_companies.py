from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ArrayWorkflowMapper
from linkedapi.types import NvSearchCompaniesParams, NvSearchCompanyResult


class NvSearchCompanies(Operation[NvSearchCompaniesParams, list[NvSearchCompanyResult]]):
    """Search companies on Sales Navigator."""

    operation_name = "nvSearchCompanies"
    mapper = ArrayWorkflowMapper[NvSearchCompaniesParams, NvSearchCompanyResult](
        "nv.searchCompanies",
        NvSearchCompanyResult,
    )
