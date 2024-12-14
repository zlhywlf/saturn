"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import pytest
from pytest_mock import MockerFixture

from saturn.__main__ import main


@pytest.mark.parametrize("has", [True, False])
def test_project_config_has_log_path(mocker: MockerFixture, *, has: bool) -> None:
    """Test project config has log path."""
    mocker.patch("saturn.__main__.Cli", return_value=mocker.Mock(start=None, stop=None))
    log_path = mocker.Mock(exists=mocker.Mock(return_value=has))
    mocker.patch("saturn.__main__.ProjectConfig", return_value=mocker.Mock(log_path=log_path))
    file_config = mocker.Mock()
    mocker.patch("saturn.__main__.logging.config", fileConfig=file_config)
    main()
    if has:
        file_config.assert_called_once_with(log_path)
    else:
        file_config.assert_not_called()


def test_start_and_stop(mocker: MockerFixture) -> None:
    """Test start and stop."""
    mocker.patch(
        "saturn.__main__.ProjectConfig",
        return_value=mocker.Mock(log_path=mocker.Mock(exists=mocker.Mock(return_value=False))),
    )
    start = mocker.Mock(app=mocker.Mock())
    stop = mocker.Mock(app=mocker.Mock())
    cli = mocker.Mock(start=start, stop=stop)
    mocker.patch("saturn.__main__.Cli", return_value=cli)
    pu = mocker.patch("saturn.__main__.ProcessUtil", return_value=mocker.Mock(start=start, stop=stop))
    main()
    start.assert_called_once()
    stop.assert_not_called()
    pu.assert_called_once_with(start.app, mocker.ANY)
    cli.start = None
    pu.reset_mock()
    stop.reset_mock()
    start.reset_mock()
    main()
    stop.assert_called_once()
    start.assert_not_called()
    pu.assert_called_once_with(stop.app, mocker.ANY)
