"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from faker import Faker
from pytest_mock import AsyncMockType, MockerFixture

from saturn.core.decisions.SimpleDecisionEngine import SimpleDecisionEngine


async def test_simple_engine(mocker: MockerFixture, faker: Faker) -> None:
    """Test simple engine."""

    def _get_return_value(v: list[str]) -> AsyncMockType:
        handle_return = mocker.AsyncMock()
        handle_return.__aiter__.return_value = v
        return handle_return  # type:ignore[no-any-return]

    sub_type = faker.random_int()
    name_root = faker.name()
    name_sub = faker.name()
    meta_root = mocker.Mock()
    meta_sub = mocker.Mock(type=sub_type)
    meta_sub.name = name_sub
    meta_root.name = name_root
    meta_root.meta = [meta_sub]
    context = mocker.Mock(checker=mocker.Mock(meta=meta_root, type=sub_type))
    handle_root = mocker.MagicMock(return_value=_get_return_value([name_root]))
    handle_sub = mocker.MagicMock(return_value=_get_return_value([name_sub]))
    engine = SimpleDecisionEngine(
        meta_root.meta,
        {
            name_root: mocker.Mock(handle=handle_root),
            name_sub: mocker.Mock(handle=handle_sub),
        },
    )
    result = [_ async for _ in engine.process(context)]
    handle_root.assert_called_once_with(context)
    handle_sub.assert_called_once_with(context)
    assert name_root == result[0]
    assert name_sub == result[1]
    context.checker.meta.name = mocker.Mock()
    handle_root.reset_mock()
    handle_sub.reset_mock()
    result = [_ async for _ in engine.process(context)]
    handle_root.assert_not_called()
    handle_sub.assert_not_called()
    assert name_root not in result
    assert name_sub not in result
