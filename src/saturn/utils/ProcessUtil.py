"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import logging.config
import platform
import queue
import subprocess  # noqa S404
import threading
from typing import ClassVar

import psutil

from saturn.configs.AppEnum import AppEnum
from saturn.configs.ProjectConfig import ProjectConfig

logger = logging.getLogger(__name__)


class ProcessUtil:
    """process util."""

    PLATFORM: ClassVar[str] = platform.system()
    APPS: ClassVar[dict[AppEnum, str]] = {AppEnum.DOC: "mkdocs serve -a 0.0.0.0:58000"}

    def __init__(self, app: AppEnum, config: ProjectConfig) -> None:
        """Init."""
        self._signal = self._handle_signal()
        self._app = app
        self._config = config
        self._signal = self._handle_signal()
        self._cmd = self.APPS[self._app]

    def _handle_signal(self) -> int:
        match self.PLATFORM:
            case "Windows" | "Darwin":
                return 15
            case "Linux":
                return 2
            case _:
                msg = f"Unsupported system environment: ({self.PLATFORM})."
                raise RuntimeError(msg)

    def start(self) -> None:  # pragma: no cover
        """Start process."""
        cmd = self._cmd
        print(self._config.project_banner)  # noqa: T201
        logger.info(f"The {self._app} will be launched through '{cmd}'")
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)  # noqa S602
        out = iter(p.stdout.readline, b"")  # type: ignore[union-attr]
        q: queue.Queue[str] = queue.Queue()
        out_thread = threading.Thread(target=lambda: [q.put(_.decode()) for _ in out])  # type: ignore[func-returns-value]
        out_thread.daemon = True
        out_thread.start()
        timeout = 5.0
        while True:
            try:
                print(q.get(timeout=timeout), end="")  # noqa: T201
                timeout = 1
            except queue.Empty:
                logger.info(f"The {self._app} has been launched")
                break

    def stop(self) -> None:
        """Close process."""
        logger.info(f"The {self._app} will be closed")
        has_closed = False
        process_keywords = self._cmd.split(" ")
        for proc in psutil.process_iter():
            if (
                proc.status() != psutil.STATUS_ZOMBIE
                and any(proc.name().startswith(_) for _ in process_keywords)
                and all(_ in proc.cmdline() for _ in process_keywords)
            ):
                proc.send_signal(self._signal)
                logger.info(f"The {self._app}:{proc.pid} has been closed")
                has_closed = True
        if not has_closed:
            logger.warning(f"The {self._app} not found")
