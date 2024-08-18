from __future__ import annotations

from typing import TYPE_CHECKING

from dataclasses import dataclass
from fs.memoryfs import MemoryFS

if TYPE_CHECKING:
    from .manifest import PackageManifest
    from .features.pkg_manager import PackageManager
    from .features.framework import Framework
    from .features.langauge import Langauge

@dataclass
class AppSpec:
    app_name: str
    pkg_name: str
    framework: Framework
    language: Langauge
    pkg_manager: PackageManager

@dataclass
class Artifact:
    fs: MemoryFS
    pkgjson: PackageManifest