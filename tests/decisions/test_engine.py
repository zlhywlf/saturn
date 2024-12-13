"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import AsyncGenerator
from typing import Any

from faker import Faker
from pytest_mock import MockerFixture

from saturn.core.data.Response import Response
from saturn.core.decisions.DecisionNode import DecisionNode
from saturn.decisions.SimpleDecisionEngine import SimpleDecisionEngine
from saturn.models.dto.decisions.Context import Context
from saturn.models.dto.decisions.Meta import Meta
from saturn.models.dto.decisions.MetaChecker import MetaChecker


async def test_engine(mocker: MockerFixture, faker: Faker) -> None:
    """Test engine."""
    node_name = faker.name()
    meta = Meta(
        id=1,
        name="test",
        type=0,
        meta=[
            Meta(
                id=2,
                name=node_name,
                type=0,
                meta=[],
                config="",
            )
        ],
        config="",
    )
    context = Context(response=mocker.create_autospec(Response), checker=MetaChecker(meta=meta, type=meta.type))

    async def _test(ctx: Context) -> AsyncGenerator[str, Any]:
        assert ctx is context
        yield node_name

    node = mocker.create_autospec(DecisionNode)
    node.handle.side_effect = _test
    engine = SimpleDecisionEngine(meta, {node_name: node})
    async for _ in engine.process(context):
        assert _ == node_name
    node.handle.assert_called_once_with(context)

    meta.meta = []
    node = mocker.create_autospec(DecisionNode)
    node.handle.return_value = mocker.AsyncMock()
    context = Context(response=mocker.create_autospec(Response), checker=MetaChecker(meta=meta, type=meta.type))
    engine = SimpleDecisionEngine(meta, {node_name: node})
    async for _ in engine.process(context):
        pass
    node.handle.assert_not_called()
