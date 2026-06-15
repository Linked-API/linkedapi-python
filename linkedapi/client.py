from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

from linkedapi.config import LinkedApiConfig
from linkedapi.errors import LinkedApiError
from linkedapi.http import HttpClient, LinkedApiHttpClient
from linkedapi.mappers import MappedResponse
from linkedapi.operations import (
    CheckConnectionStatus,
    CommentOnPost,
    CreatePost,
    CustomWorkflow,
    FetchCompany,
    FetchPerson,
    FetchPost,
    NvFetchCompany,
    NvFetchPerson,
    NvSearchCompanies,
    NvSearchPeople,
    NvSendMessage,
    NvSyncConversation,
    ReactToPost,
    RemoveConnection,
    RetrieveConnections,
    RetrievePendingRequests,
    RetrievePerformance,
    RetrieveSSI,
    SearchCompanies,
    SearchPeople,
    SendConnectionRequest,
    SendMessage,
    SyncConversation,
    WithdrawConnectionRequest,
)
from linkedapi.types import AccountInfo, LinkedApiActionError, serialize_value
from linkedapi.types.message import ConversationPollRequest, ConversationPollResult
from linkedapi.types.statistics import ApiUsageAction, ApiUsageParams


class LinkedApi:
    """Official synchronous Python SDK for Linked API."""

    def __init__(self, config: LinkedApiConfig | HttpClient[Any]) -> None:
        self.http_client = (
            config
            if isinstance(config, HttpClient)
            else LinkedApiHttpClient(config, config.client, config.base_url)
        )

        self.custom_workflow = CustomWorkflow(self.http_client)
        self.send_message = SendMessage(self.http_client)
        self.sync_conversation = SyncConversation(self.http_client)
        self.check_connection_status = CheckConnectionStatus(self.http_client)
        self.send_connection_request = SendConnectionRequest(self.http_client)
        self.withdraw_connection_request = WithdrawConnectionRequest(self.http_client)
        self.retrieve_pending_requests = RetrievePendingRequests(self.http_client)
        self.retrieve_connections = RetrieveConnections(self.http_client)
        self.remove_connection = RemoveConnection(self.http_client)
        self.search_companies = SearchCompanies(self.http_client)
        self.search_people = SearchPeople(self.http_client)
        self.fetch_company = FetchCompany(self.http_client)
        self.fetch_person = FetchPerson(self.http_client)
        self.fetch_post = FetchPost(self.http_client)
        self.react_to_post = ReactToPost(self.http_client)
        self.comment_on_post = CommentOnPost(self.http_client)
        self.create_post = CreatePost(self.http_client)
        self.retrieve_ssi = RetrieveSSI(self.http_client)
        self.retrieve_performance = RetrievePerformance(self.http_client)
        self.nv_send_message = NvSendMessage(self.http_client)
        self.nv_sync_conversation = NvSyncConversation(self.http_client)
        self.nv_search_companies = NvSearchCompanies(self.http_client)
        self.nv_search_people = NvSearchPeople(self.http_client)
        self.nv_fetch_company = NvFetchCompany(self.http_client)
        self.nv_fetch_person = NvFetchPerson(self.http_client)

        self.operations = [
            self.custom_workflow,
            self.send_message,
            self.sync_conversation,
            self.check_connection_status,
            self.send_connection_request,
            self.withdraw_connection_request,
            self.retrieve_pending_requests,
            self.retrieve_connections,
            self.remove_connection,
            self.search_companies,
            self.search_people,
            self.fetch_company,
            self.fetch_person,
            self.fetch_post,
            self.react_to_post,
            self.comment_on_post,
            self.create_post,
            self.retrieve_ssi,
            self.retrieve_performance,
            self.nv_send_message,
            self.nv_sync_conversation,
            self.nv_search_companies,
            self.nv_search_people,
            self.nv_fetch_company,
            self.nv_fetch_person,
        ]

    def poll_conversations(
        self,
        conversations: list[ConversationPollRequest],
    ) -> MappedResponse[list[ConversationPollResult]]:
        """Poll previously synced standard or Sales Navigator conversations."""

        try:
            response = self.http_client.post("/conversations/poll", serialize_value(conversations))
            if response.success and response.result is not None:
                return MappedResponse(
                    data=[ConversationPollResult.model_validate(item) for item in response.result],
                    errors=[],
                )
            return MappedResponse(
                data=None,
                errors=[
                    LinkedApiActionError(
                        type=response.error.type if response.error else "",
                        message=response.error.message if response.error else "",
                    ),
                ],
            )
        except LinkedApiError as error:
            if error.type == "conversationsNotSynced":
                return MappedResponse(
                    data=None,
                    errors=[LinkedApiActionError(type=error.type, message=error.message)],
                )
            raise

    def get_account_info(self) -> MappedResponse[AccountInfo]:
        """Retrieve basic information about the current LinkedIn account."""

        response = self.http_client.get("/account")
        if response.success and response.result is not None:
            return MappedResponse(data=AccountInfo.model_validate(response.result), errors=[])
        raise LinkedApiError(
            response.error.type if response.error else "httpError",
            response.error.message if response.error else "",
        )

    def get_api_usage(self, params: ApiUsageParams) -> MappedResponse[list[ApiUsageAction]]:
        """Retrieve Linked API action usage statistics for a time period."""

        query_params = urlencode({"start": params.start, "end": params.end})
        response = self.http_client.get(f"/stats/actions?{query_params}")
        if response.success and response.result is not None:
            return MappedResponse(
                data=[ApiUsageAction.model_validate(item) for item in response.result],
                errors=[],
            )
        raise LinkedApiError(
            response.error.type if response.error else "httpError",
            response.error.message if response.error else "",
        )
