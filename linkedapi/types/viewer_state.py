from __future__ import annotations

from typing import Literal

from linkedapi.types.base import LinkedApiModel

# Your connection degree to a person, as LinkedIn shows it next to their name.
ConnectionDegree = Literal["1st", "2nd", "3rd+"]
# Sales Navigator also filters by members of the groups you belong to.
NvConnectionDegreeFilter = Literal["1st", "2nd", "3rd+", "groupMembers"]


class PersonViewerState(LinkedApiModel):
    """How your account relates to a person.

    "connection_degree" is None when LinkedIn shows no degree, e.g. on your own content.
    """

    connection_degree: ConnectionDegree | None = None
