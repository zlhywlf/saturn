"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from pydantic import BaseModel


class NodeConfig(BaseModel):
    """node config."""

    needed: bool = False
