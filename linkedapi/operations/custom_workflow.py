from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import BaseMapper, MappedResponse
from linkedapi.types import WorkflowCompletion, WorkflowDefinition


class _CustomWorkflowMapper(BaseMapper[WorkflowDefinition, WorkflowCompletion]):
    def map_request(self, params: WorkflowDefinition | None = None) -> WorkflowDefinition:
        if params is None:
            return {}
        return params

    def map_response(self, completion: WorkflowCompletion) -> MappedResponse[WorkflowCompletion]:
        return MappedResponse(data=completion, errors=[])


class CustomWorkflow(Operation[WorkflowDefinition, WorkflowCompletion]):
    """Execute raw Linked API workflow definitions."""

    operation_name = "customWorkflow"
    mapper = _CustomWorkflowMapper()
