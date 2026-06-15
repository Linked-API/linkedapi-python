from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ActionConfig, ResponseMapping, ThenWorkflowMapper
from linkedapi.types import FetchPersonParams, Person


class FetchPersonMapper(ThenWorkflowMapper[FetchPersonParams, Person]):
    def __init__(self) -> None:
        super().__init__(
            action_configs=[
                ActionConfig("retrieve_experience", "st.retrievePersonExperience"),
                ActionConfig("retrieve_education", "st.retrievePersonEducation"),
                ActionConfig("retrieve_skills", "st.retrievePersonSkills"),
                ActionConfig("retrieve_languages", "st.retrievePersonLanguages"),
                ActionConfig("retrieve_posts", "st.retrievePersonPosts", "posts_retrieval_config"),
                ActionConfig(
                    "retrieve_comments", "st.retrievePersonComments", "comments_retrieval_config"
                ),
                ActionConfig(
                    "retrieve_reactions", "st.retrievePersonReactions", "reactions_retrieval_config"
                ),
            ],
            response_mappings=[
                ResponseMapping("st.retrievePersonExperience", "experiences"),
                ResponseMapping("st.retrievePersonEducation", "education"),
                ResponseMapping("st.retrievePersonSkills", "skills"),
                ResponseMapping("st.retrievePersonLanguages", "languages"),
                ResponseMapping("st.retrievePersonPosts", "posts"),
                ResponseMapping("st.retrievePersonComments", "comments"),
                ResponseMapping("st.retrievePersonReactions", "reactions"),
            ],
            base_action_type="st.openPersonPage",
            default_params={"basicInfo": True},
            result_model=Person,
        )


class FetchPerson(Operation[FetchPersonParams, Person]):
    """Fetch a standard LinkedIn person profile."""

    operation_name = "fetchPerson"
    mapper = FetchPersonMapper()
