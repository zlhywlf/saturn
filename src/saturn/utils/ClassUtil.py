"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import Generator
from importlib import import_module
from importlib.resources import files
from importlib.resources.abc import Traversable
from types import ModuleType
from typing import Any


def get_modules(pkg: str) -> Generator[ModuleType | None, Any, None]:
    """Get modules."""

    def get_module(module_meta: Traversable) -> ModuleType | None:
        """Get module."""
        name, point, suffix = module_meta.name.rpartition(".")
        if not module_meta.is_file() or suffix != "py":
            return None
        try:
            return import_module(f"{point}{name}", pkg)
        except ModuleNotFoundError:
            return None

    return (get_module(module_meta) for module_meta in files(pkg).iterdir())


def find_class_by_type[T](module: ModuleType | None, super_type: T) -> list[T]:
    """Find class by type."""
    if not module or not isinstance(super_type, type):
        return []
    ret: list[T] = []
    for cls in module.__dict__.values():
        if not isinstance(cls, type) or cls is super_type or not issubclass(cls, super_type):
            continue
        ret.append(cls)  # type: ignore[arg-type]
    return ret


def get_special_modules[T](package_name: str, super_type: T) -> list[T]:
    """Get special modules."""
    ret: list[T] = []
    for m in get_modules(package_name):
        ret.extend(find_class_by_type(m, super_type))
    return ret
