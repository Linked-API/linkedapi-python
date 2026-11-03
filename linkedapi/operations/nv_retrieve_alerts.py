from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ArrayWorkflowMapper
from linkedapi.types import NvAlert, NvRetrieveAlertsParams


class NvRetrieveAlerts(Operation[NvRetrieveAlertsParams, list[NvAlert]]):
    """Retrieve Sales Navigator lead and account alerts."""

    operation_name = "nvRetrieveAlerts"
    mapper = ArrayWorkflowMapper[NvRetrieveAlertsParams, NvAlert]("nv.retrieveAlerts", NvAlert)
