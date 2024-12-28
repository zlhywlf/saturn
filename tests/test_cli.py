import sys
from io import StringIO

import pytest
from faker import Faker
from pytest_mock import MockerFixture

from saturn.cli.Root import Root
from saturn.configs.AppEnum import AppEnum


@pytest.mark.parametrize("arg", ["-V", "--version"])
def test_version(mocker: MockerFixture, faker: Faker, arg: str) -> None:
    """Test version."""
    v = faker.name()
    mocker.patch("saturn.cli.Root.version", v)
    exit_ = mocker.patch("argparse.ArgumentParser.exit")
    out = mocker.patch("sys.stdout", new_callable=StringIO)
    sys.argv = ["_", arg]
    Root()
    assert v in out.getvalue()
    assert exit_.called


@pytest.mark.parametrize("arg", ["-h", "--help", ""])
def test_help(mocker: MockerFixture, arg: str) -> None:
    """Test help."""
    exit_ = mocker.patch("argparse.ArgumentParser.exit")
    out = mocker.patch("sys.stdout", new_callable=StringIO)
    sys.argv = ["_"] + ([arg] if arg else [])
    Root()
    assert "usage" in out.getvalue()
    assert exit_.called


def test_start() -> None:
    """Test start."""
    sys.argv = ["_", "start", "--app", AppEnum.DOC]
    cli = Root()
    assert cli.start
    assert cli.start.app == AppEnum.DOC


def test_stop() -> None:
    """Test stop."""
    sys.argv = ["_", "stop", "--app", AppEnum.DOC]
    cli = Root()
    assert cli.stop
    assert cli.stop.app == AppEnum.DOC
