from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

from linkedapi.config import LinkedApiConfig
from linkedapi.errors import LinkedApiError
from linkedapi.http import HttpClient, LinkedApiHttpClient
from linkedapi.mappers import MappedResponse
from linkedapi.operations import (
    AcceptInvitation,
    CheckConnectionStatus,
    CommentOnPost,
    CreatePost,
    CustomWorkflow,
    FetchCompany,
    FetchJob,
    FetchPerson,
    FetchPost,
    IgnoreInvitation,
    ManageConversation,
    NvFetchCompany,
    NvFetchPerson,
    NvManageConversation,
    NvSearchCompanies,
    NvSearchPeople,
    NvSendMessage,
    NvSyncConversation,
    NvSyncInbox,
    ReactToComment,
    ReactToPost,
    RemoveConnection,
    ReplyToComment,
    RetrieveConnections,
    RetrieveFeed,
    RetrieveInvitations,
    RetrievePendingRequests,
    RetrievePerformance,
    RetrieveSSI,
    SearchCompanies,
    SearchJobs,
    SearchPeople,
    SendConnectionRequest,
    SendMessage,
    SyncConversation,
    SyncInbox,
    SyncNetwork,
    WithdrawConnectionRequest,
)
from linkedapi.types import AccountInfo, LinkedApiActionError, serialize_value
from linkedapi.types.message import (
    ConversationPollRequest,
    ConversationPollResult,
    InboxMessage,
    InboxPollRequest,
)
from linkedapi.types.network import NetworkEvent, NetworkPollRequest
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
        self.sync_inbox = SyncInbox(self.http_client)
        self.sync_network = SyncNetwork(self.http_client)
        self.manage_conversation = ManageConversation(self.http_client)
        self.check_connection_status = CheckConnectionStatus(self.http_client)
        self.send_connection_request = SendConnectionRequest(self.http_client)
        self.withdraw_connection_request = WithdrawConnectionRequest(self.http_client)
        self.accept_invitation = AcceptInvitation(self.http_client)
        self.ignore_invitation = IgnoreInvitation(self.http_client)
        self.retrieve_pending_requests = RetrievePendingRequests(self.http_client)
        self.retrieve_invitations = RetrieveInvitations(self.http_client)
        self.retrieve_connections = RetrieveConnections(self.http_client)
        self.remove_connection = RemoveConnection(self.http_client)
        self.search_companies = SearchCompanies(self.http_client)
        self.search_people = SearchPeople(self.http_client)
        self.search_jobs = SearchJobs(self.http_client)
        self.fetch_company = FetchCompany(self.http_client)
        self.fetch_person = FetchPerson(self.http_client)
        self.fetch_post = FetchPost(self.http_client)
        self.fetch_job = FetchJob(self.http_client)
        self.react_to_post = ReactToPost(self.http_client)
        self.comment_on_post = CommentOnPost(self.http_client)
        self.react_to_comment = ReactToComment(self.http_client)
        self.reply_to_comment = ReplyToComment(self.http_client)
        self.create_post = CreatePost(self.http_client)
        self.retrieve_feed = RetrieveFeed(self.http_client)
        self.retrieve_ssi = RetrieveSSI(self.http_client)
        self.retrieve_performance = RetrievePerformance(self.http_client)
        self.nv_send_message = NvSendMessage(self.http_client)
        self.nv_sync_conversation = NvSyncConversation(self.http_client)
        self.nv_sync_inbox = NvSyncInbox(self.http_client)
        self.nv_manage_conversation = NvManageConversation(self.http_client)
        self.nv_search_companies = NvSearchCompanies(self.http_client)
        self.nv_search_people = NvSearchPeople(self.http_client)
        self.nv_fetch_company = NvFetchCompany(self.http_client)
        self.nv_fetch_person = NvFetchPerson(self.http_client)

        self.operations = [
            self.custom_workflow,
            self.send_message,
            self.sync_conversation,
            self.sync_inbox,
            self.sync_network,
            self.manage_conversation,
            self.check_connection_status,
            self.send_connection_request,
            self.withdraw_connection_request,
            self.accept_invitation,
            self.ignore_invitation,
            self.retrieve_pending_requests,
            self.retrieve_invitations,
            self.retrieve_connections,
            self.remove_connection,
            self.search_companies,
            self.search_people,
            self.search_jobs,
            self.fetch_company,
            self.fetch_person,
            self.fetch_post,
            self.fetch_job,
            self.react_to_post,
            self.comment_on_post,
            self.react_to_comment,
            self.reply_to_comment,
            self.create_post,
            self.retrieve_feed,
            self.retrieve_ssi,
            self.retrieve_performance,
            self.nv_send_message,
            self.nv_sync_conversation,
            self.nv_sync_inbox,
            self.nv_manage_conversation,
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

    def poll_inbox(
        self,
        request: InboxPollRequest | None = None,
    ) -> MappedResponse[list[InboxMessage]]:
        """Read the monitored standard or Sales Navigator inbox, newest messages first."""

        payload = serialize_value(request) if request is not None else {}
        response = self.http_client.post("/inbox/poll", payload)
        if response.success and response.result is not None:
            messages = response.result.get("messages", [])
            return MappedResponse(
                data=[InboxMessage.model_validate(item) for item in messages],
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

    def poll_network(
        self,
        request: NetworkPollRequest | None = None,
    ) -> MappedResponse[list[NetworkEvent]]:
        """Read the monitored network connection events, newest events first."""

        payload = serialize_value(request) if request is not None else {}
        response = self.http_client.post("/network/poll", payload)
        if response.success and response.result is not None:
            events = response.result.get("events", [])
            return MappedResponse(
                data=[NetworkEvent.model_validate(item) for item in events],
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
