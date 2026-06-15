from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from linkedapi.types.responses import LinkedApiResponse

TResult = TypeVar("TResult")


class HttpClient(ABC, Generic[TResult]):
    @abstractmethod
    def get(self, path: str) -> LinkedApiResponse[Any]:
        raise NotImplementedError

    @abstractmethod
    def post(self, path: str, data: Any | None = None) -> LinkedApiResponse[Any]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, path: str) -> LinkedApiResponse[Any]:
        raise NotImplementedError
