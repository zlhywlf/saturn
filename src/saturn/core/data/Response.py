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
    async def extract(self, query: str) -> SelectorList[Selector]:
        """Extract."""

    @property
    @abstractmethod
    async def url(self) -> str:
        """Url."""

    @property
    @abstractmethod
    def is_json(self) -> bool:
        """Is json."""

    @abstractmethod
    async def replace(self, body: bytes) -> None:
        """Replace."""
