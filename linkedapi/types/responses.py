from __future__ import annotations

from typing import Generic, TypeVar

from linkedapi.types.base import LinkedApiModel

TResult = TypeVar("TResult")


class LinkedApiRequestError(LinkedApiModel):
    type: str
    message: str


class LinkedApiResponse(LinkedApiModel, Generic[TResult]):
    success: bool
    result: TResult | None = None
    error: LinkedApiRequestError | None = None
