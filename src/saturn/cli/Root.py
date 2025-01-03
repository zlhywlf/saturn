import sys
from argparse import ArgumentParser

from pydantic import Field
from pydantic_settings import BaseSettings, CliSettingsSource, CliSubCommand

from saturn._version import version
from saturn.cli.Start import Start
from saturn.cli.Stop import Stop


class Root(BaseSettings):
    """root."""

    start: CliSubCommand[Start] = Field(description="start")
    stop: CliSubCommand[Stop] = Field(description="stop")

    def __init__(self) -> None:
        """Init."""
        if not sys.argv[1:]:
            sys.argv.append("-h")
        super().__init__(_cli_settings_source=self._create_cli_settings_source("saturn"))

    def _create_cli_settings_source(self, prog: str) -> CliSettingsSource[ArgumentParser]:
        description = "The powerful crawler application"
        arg_parser = ArgumentParser(prog=prog, description=description)
        help_msg = "show this version information and exit"
        arg_parser.add_argument("-V", "--version", action="version", version=version, help=help_msg)
        return CliSettingsSource(
            self.__class__,
            cli_parse_args=True,
            root_parser=arg_parser,
            parse_args_method=lambda parser, args: parser.parse_known_args(args)[0],
        )
