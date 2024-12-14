"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import pathlib

from faker import Faker
from pytest_mock import MockerFixture

from saturn.configs.ProjectConfig import ProjectConfig


def test_project_banner(tmp_path: pathlib.Path, mocker: MockerFixture, faker: Faker) -> None:
    """Test project banner."""
    version = faker.name()
    mocker.patch("saturn.configs.ProjectConfig.version", version)
    config = ProjectConfig(banner_path=tmp_path / faker.name())
    assert config.debug
    assert version in config.project_banner  # type:ignore[operator]
    assert config.banner == ProjectConfig.default_banner()
    banner = faker.text()
    p = tmp_path / faker.name()
    p.write_text(banner)
    config = ProjectConfig(banner_path=p)
    assert config.banner == banner
    config = ProjectConfig(banner=banner)
    assert config.banner == banner
