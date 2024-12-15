"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod


class RfpPersistentSync(ABC):
    """request fingerprint persistent."""

    @abstractmethod
    def save(self, key: str, data: str) -> int:
        """Save."""

    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete."""

    @abstractmethod
    def exist(self, key: str, data: str) -> bool:
        """Exist."""
