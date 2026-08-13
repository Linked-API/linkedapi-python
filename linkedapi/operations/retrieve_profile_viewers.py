from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ArrayWorkflowMapper
from linkedapi.types import ProfileViewer, RetrieveProfileViewersParams


class RetrieveProfileViewers(Operation[RetrieveProfileViewersParams, list[ProfileViewer]]):
    """Retrieve the viewers visible on the current account's LinkedIn profile."""

    operation_name = "retrieveProfileViewers"
    mapper = ArrayWorkflowMapper[RetrieveProfileViewersParams, ProfileViewer](
        "st.retrieveProfileViewers",
        ProfileViewer,
    )
