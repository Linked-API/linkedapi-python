from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ArrayWorkflowMapper
from linkedapi.types import SearchJobResult, SearchJobsParams


class SearchJobs(Operation[SearchJobsParams, list[SearchJobResult]]):
    """Search jobs on standard LinkedIn."""

    operation_name = "searchJobs"
    mapper = ArrayWorkflowMapper[SearchJobsParams, SearchJobResult](
        "st.searchJobs",
        SearchJobResult,
    )
