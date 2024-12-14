"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import logging
import logging.config

from saturn.cli.Root import Root as Cli
from saturn.configs.ProjectConfig import ProjectConfig
from saturn.utils.ProcessUtil import ProcessUtil


def main() -> None:
    """The powerful crawler application."""
    cli = Cli()
    config = ProjectConfig()
    if config.log_path.exists():
        logging.config.fileConfig(config.log_path)
    if cli.start:
        ProcessUtil(cli.start.app, config).start()
        return
    if cli.stop:
        ProcessUtil(cli.stop.app, config).stop()


if __name__ == "__main__":
    main()
