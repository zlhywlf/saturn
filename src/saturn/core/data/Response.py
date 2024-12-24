"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod
from typing import Any

from parsel.selector import Selector, SelectorList


class Response(ABC):
    """response."""

    @abstractmethod
    async def urljoin(self, url: str) -> str:
        """Urljoin."""

    @property
    @abstractmethod
    async def text(self) -> str:
        """Text."""

    @property
    @abstractmethod
    async def headers(self) -> dict[str, bytes]:
        """Headers."""

    @property
    @abstractmethod
    async def body(self) -> bytes:
        """Body."""

    @property
    @abstractmethod
    async def meta(self) -> dict[str, Any]:
        """Meta."""

    @abstractmethod
    async def extract_by_xpath(self, query: str) -> SelectorList[Selector]:
        """Extract by xpath."""

    @property
    @abstractmethod
    async def url(self) -> str:
        """Url."""

    @abstractmethod
    async def extract_by_jmespath(self, query: str) -> SelectorList[Selector]:
        """Extract by jmespath."""
