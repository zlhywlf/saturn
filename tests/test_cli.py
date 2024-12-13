"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import subprocess  # noqa S404
import sys

import pytest
from pytest_mock import MockerFixture

from saturn._version import version
from io import StringIO
from saturn.__main__ import main
from saturn.configs.AppEnum import AppEnum


@pytest.mark.parametrize(
    "args",
    [
        ("-V", version),
        ("--version", version),
        ("", "usage"),
        ("-h", "usage"),
        ("--help", "usage"),
    ],
    ids=lambda a: a[0],
)
def test_version_and_help(mocker: MockerFixture, args: tuple[str, str]) -> None:
    """Test version and help."""
    arg, expected = args
    exit_ = mocker.patch("argparse.ArgumentParser.exit")
    out = mocker.patch("sys.stdout", new_callable=StringIO)
    sys.argv = ["_"] + ([arg] if arg else [])
    main()
    assert expected in out.getvalue()
    assert exit_.called


@pytest.mark.parametrize(
    "cmd",
    [
        "start",
        "stop",
    ],
)
def test_start_and_stop(mocker: MockerFixture, cmd: str) -> None:
    """Test start and stop."""
    fn = mocker.patch(f"saturn.utils.ProcessUtil.ProcessUtil.{cmd}")
    sys.argv = ["_", cmd, "--app", AppEnum.DOC]
    main()
    assert fn.called
