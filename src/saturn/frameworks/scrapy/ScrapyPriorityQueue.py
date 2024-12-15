"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Any, override

from pydantic import TypeAdapter
from scrapy import Spider

from saturn.core.queues.Queue import Queue
from saturn.core.queues.QueuePersistentSync import QueuePersistentSync
from saturn.models.dto.decisions.Task import Task


class ScrapyPriorityQueue(Queue):
    """scrapy priority queue."""

    def __init__(self, qp: QueuePersistentSync, spider: Spider, key: str) -> None:
        """Init."""
        self._type_adapter = TypeAdapter(dict[str, Any])
        self._spider = spider
        self._key = key
        self._qp = qp

    @override
    def encode_task(self, task: Task) -> bytes:
        return task.model_dump_json(by_alias=True).encode()

    @override
    def decode_task(self, encoded_task: bytes) -> Task:
        return Task.model_validate_json(encoded_task)

    @override
    def __len__(self) -> int:
        return self._qp.get_length(self._key)

    @override
    def push(self, task: Task) -> None:
        data = self.encode_task(task)
        self._qp.save(self._key, data, task.priority)

    @override
    def pop(self) -> Task | None:
        results = self._qp.select(self._key, 0, 0, -1, -1)
        return self.decode_task(results[0]) if results else None

    @override
    def clear(self) -> None:
        self._qp.delete(self._key)
