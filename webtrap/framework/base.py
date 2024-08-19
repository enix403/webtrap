from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from webtrap.options import Artifact, AppSpec

class BaseFramework:
    def __init__(self):
        pass

    def add_import(self):
        pass

    def add_effect_import(self):
        pass

    def finalize(self, spec: AppSpec, artifact: Artifact):
        pass