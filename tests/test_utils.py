"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Any

import pytest
from faker import Faker
from pytest_mock import MockerFixture

from saturn.configs.AppEnum import AppEnum
from saturn.configs.ProjectConfig import ProjectConfig
from saturn.utils.ProcessUtil import ProcessUtil


@pytest.mark.parametrize(
    ("arg", "signal"),
    [
        ("Windows", 15),
        ("Linux", 2),
        ("Darwin", 15),
        pytest.param("NOP", -1, marks=pytest.mark.xfail(raises=RuntimeError)),
    ],
)
def test_process_manager_signal(arg: str, signal: int, mocker: MockerFixture) -> None:
    """Test process manager signal."""
    mocker.patch.object(ProcessUtil, "PLATFORM", new=arg)
    p = ProcessUtil(AppEnum.DOC, ProjectConfig())
    assert p._signal == signal


def test_process_manager_start(capsys: pytest.CaptureFixture[str], faker: Faker) -> None:
    """Test process manager start."""
    key = faker.name()
    p = ProcessUtil(AppEnum.DOC, ProjectConfig())
    p._cmd = " ".join(["echo", key])
    p.start()
    assert key in capsys.readouterr().out


@pytest.fixture(scope="module")
def process_util() -> ProcessUtil:
    """Process util."""
    return ProcessUtil(AppEnum.DOC, ProjectConfig())


@pytest.fixture
def process_obj() -> object:
    """Process obj."""
    return type("FakeProcess", (), {})


def test_process_manager_stop_success(process_util: ProcessUtil, mocker: MockerFixture, process_obj: Any) -> None:  # noqa ANN401
    """Test process manager stop success."""
    process_obj.status = lambda: "running"
    process_obj.name = lambda: "mkdocs.exe"
    process_obj.cmdline = lambda: process_util._cmd.split(" ")
    process_obj.send_signal = lambda s: s
    process_obj.pid = 0
    mocker.patch("psutil.process_iter", return_value=[process_obj])
    send_signal = mocker.patch.object(process_obj, "send_signal")
    process_util.stop()
    send_signal.assert_called_once_with(process_util._signal)


@pytest.mark.parametrize(
    ("name", "cmd", "status"),
    [
        ("NOP", [], ""),
        ("mkdocs.exe", ["NOP"], ""),
    ],
)
def test_process_manager_stop_failure(
    process_util: ProcessUtil,
    process_obj: Any,  # noqa ANN401
    mocker: MockerFixture,
    name: str,
    cmd: list[str],
    status: str,
) -> None:
    """Test process manager stop failure."""
    process_obj.send_signal = lambda s: s
    process_obj.status = lambda: status
    process_obj.name = lambda: name
    process_obj.cmdline = lambda: cmd
    mocker.patch("psutil.process_iter", return_value=[process_obj])
    send_signal = mocker.patch.object(process_obj, "send_signal")
    process_util.stop()
    send_signal.assert_not_called()
