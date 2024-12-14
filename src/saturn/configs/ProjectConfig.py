"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import logging
import pathlib

from pydantic import Field, ValidationInfo, computed_field, field_validator
from pydantic_settings import BaseSettings

from saturn._version import version

logger = logging.getLogger(__name__)


class ProjectConfig(BaseSettings, env_prefix="SATURN_", env_file=".env", env_file_encoding="utf-8"):
    """project config."""

    banner_path: pathlib.Path = Field(default=pathlib.Path.cwd() / "banner.txt", description="banner file path")
    banner: str = Field(default="", description="banner")
    debug: bool = Field(default=False, description="debug mode")
    log_path: pathlib.Path = Field(default=pathlib.Path.cwd() / "logging.ini", description="log config path")

    @computed_field
    def project_banner(self) -> str:
        """Project banner."""
        return f"{self.banner}\n:: the powerful crawler application :: v{version}\n"

    @field_validator("banner")
    @classmethod
    def inject_banner(cls, v: str, info: ValidationInfo) -> str:
        """Inject banner."""
        if v:
            return v
        banner_path = info.data["banner_path"]
        if not banner_path.exists():
            return cls.default_banner()
        with banner_path.open("r") as f:
            return "".join(f.readlines())

    @classmethod
    def default_banner(cls) -> str:
        """Default banner."""
        return r"""
 ::::::::      ::: ::::::::::: :::    ::: :::::::::  ::::    :::
:+:    :+:   :+: :+:   :+:     :+:    :+: :+:    :+: :+:+:   :+:
+:+         +:+   +:+  +:+     +:+    +:+ +:+    +:+ :+:+:+  +:+
+#++:++#++ +#++:++#++: +#+     +#+    +:+ +#++:++#:  +#+ +:+ +#+
       +#+ +#+     +#+ +#+     +#+    +#+ +#+    +#+ +#+  +#+#+#
#+#    #+# #+#     #+# #+#     #+#    #+# #+#    #+# #+#   #+#+#
 ########  ###     ### ###      ########  ###    ### ###    ####
"""
