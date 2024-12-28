import shutil
import subprocess
from pathlib import Path
from typing import Any, override

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class FrontendBuildHook(BuildHookInterface):
    @override
    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        print(build_data)
        try:
            subprocess.run(["pnpm", "build"], check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print("Error during pnpm build:", e)
            exit(1)
        source_dir = Path("dist")
        target_dir = Path("src/saturn/web/templates")
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.rmtree(target_dir)
        for file_path in source_dir.iterdir():
            if file_path.is_file():
                target_path = target_dir / file_path.name
                file_path.rename(target_path)
            elif file_path.is_dir():
                shutil.move(file_path, target_dir / file_path.name)
