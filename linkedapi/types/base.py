from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


def to_camel(value: str) -> str:
    parts = value.split("_")
    return parts[0] + "".join(part.capitalize() for part in parts[1:])


class LinkedApiModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


def serialize_value(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return value.model_dump(by_alias=True, exclude_none=True)
    if isinstance(value, list):
        return [serialize_value(item) for item in value]
    if isinstance(value, tuple):
        return [serialize_value(item) for item in value]
    if isinstance(value, dict):
        return {key: serialize_value(item) for key, item in value.items() if item is not None}
    return value


def serialize_model(value: Any) -> dict[str, Any]:
    serialized = serialize_value(value)
    if serialized is None:
        return {}
    if isinstance(serialized, dict):
        return serialized
    msg = "Expected object-like parameters"
    raise TypeError(msg)


def dump_model_by_name(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, BaseModel):
        return value.model_dump(by_alias=False, exclude_none=True)
    if isinstance(value, dict):
        return {str(key): item for key, item in value.items() if item is not None}
    msg = "Expected object-like parameters"
    raise TypeError(msg)
