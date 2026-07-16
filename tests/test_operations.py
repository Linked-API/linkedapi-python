from __future__ import annotations

from conftest import FakeHttpClient

from linkedapi import (
    ArrayWorkflowMapper,
    FetchPersonParams,
    LinkedApi,
    LinkedApiConfig,
    VoidWorkflowMapper,
)


def test_linked_api_exposes_all_predefined_operations() -> None:
    linkedapi = LinkedApi(LinkedApiConfig(linked_api_token="x", identification_token="y"))
    operation_names = [
        "custom_workflow",
        "fetch_person",
        "nv_fetch_person",
        "fetch_company",
        "nv_fetch_company",
        "fetch_post",
        "fetch_job",
        "search_people",
        "nv_search_people",
        "search_companies",
        "nv_search_companies",
        "search_jobs",
        "send_connection_request",
        "check_connection_status",
        "withdraw_connection_request",
        "accept_connection_request",
        "ignore_connection_request",
        "retrieve_pending_requests",
        "retrieve_connection_requests",
        "retrieve_connections",
        "remove_connection",
        "send_message",
        "sync_conversation",
        "sync_inbox",
        "sync_network",
        "manage_conversation",
        "nv_send_message",
        "nv_sync_conversation",
        "nv_sync_inbox",
        "nv_manage_conversation",
        "react_to_post",
        "comment_on_post",
        "create_post",
        "retrieve_ssi",
        "retrieve_performance",
    ]

    for name in operation_names:
        operation = getattr(linkedapi, name)
        assert hasattr(operation, "execute")
        assert hasattr(operation, "result")
        assert hasattr(operation, "cancel")
    assert len(linkedapi.operations) == 35


def test_operation_mappers_match_node_contract() -> None:
    linkedapi = LinkedApi(LinkedApiConfig(linked_api_token="x", identification_token="y"))

    assert linkedapi.fetch_person.mapper.base_action_type == "st.openPersonPage"
    assert linkedapi.fetch_person.mapper.default_params == {"basicInfo": True}
    assert isinstance(linkedapi.search_people.mapper, ArrayWorkflowMapper)
    assert linkedapi.search_people.mapper.base_action_type == "st.searchPeople"
    assert isinstance(linkedapi.search_jobs.mapper, ArrayWorkflowMapper)
    assert linkedapi.search_jobs.mapper.base_action_type == "st.searchJobs"
    assert linkedapi.fetch_job.mapper.base_action_type == "st.openJob"
    assert linkedapi.fetch_job.mapper.default_params == {"basicInfo": True}
    assert isinstance(linkedapi.send_connection_request.mapper, VoidWorkflowMapper)
    assert linkedapi.send_connection_request.mapper.action_type == "st.sendConnectionRequest"
    assert isinstance(linkedapi.accept_connection_request.mapper, VoidWorkflowMapper)
    assert linkedapi.accept_connection_request.mapper.action_type == "st.acceptConnectionRequest"
    assert isinstance(linkedapi.ignore_connection_request.mapper, VoidWorkflowMapper)
    assert linkedapi.ignore_connection_request.mapper.action_type == "st.ignoreConnectionRequest"
    assert isinstance(linkedapi.retrieve_connection_requests.mapper, ArrayWorkflowMapper)
    assert (
        linkedapi.retrieve_connection_requests.mapper.base_action_type
        == "st.retrieveConnectionRequests"
    )
    assert isinstance(linkedapi.sync_inbox.mapper, VoidWorkflowMapper)
    assert linkedapi.sync_inbox.mapper.action_type == "st.syncInbox"
    assert isinstance(linkedapi.nv_sync_inbox.mapper, VoidWorkflowMapper)
    assert linkedapi.nv_sync_inbox.mapper.action_type == "nv.syncInbox"
    assert isinstance(linkedapi.manage_conversation.mapper, VoidWorkflowMapper)
    assert linkedapi.manage_conversation.mapper.action_type == "st.manageConversation"
    assert isinstance(linkedapi.nv_manage_conversation.mapper, VoidWorkflowMapper)
    assert linkedapi.nv_manage_conversation.mapper.action_type == "nv.manageConversation"


def test_execute_and_result_flow_returns_pydantic_data(
    fake_http_client: FakeHttpClient,
    person_data: dict[str, object],
) -> None:
    linkedapi = LinkedApi(fake_http_client)
    fake_http_client.queue_response(result={"workflowId": "wf1", "workflowStatus": "pending"})
    fake_http_client.queue_response(
        result={
            "workflowId": "wf1",
            "workflowStatus": "completed",
            "completion": {
                "actionType": "st.openPersonPage",
                "success": True,
                "data": person_data,
            },
        }
    )

    workflow = linkedapi.fetch_person.execute(FetchPersonParams(person_url="u"))
    result = linkedapi.fetch_person.result(workflow.workflow_id, poll_interval=0.001, timeout=1.0)

    assert fake_http_client.calls[0] == (
        "POST",
        "/workflows",
        {
            "actionType": "st.openPersonPage",
            "basicInfo": True,
            "personUrl": "u",
            "then": [],
        },
    )
    assert result.data is not None
    assert result.data.public_url == "https://www.linkedin.com/in/jane-doe"
