from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

from webtrap.printers import Printer

if TYPE_CHECKING:
    from webtrap.options import Artifact, AppSpec


STYLESHEET_RESET = 0
STYLESHEET_LIBRARY = 1
STYLESHEET_OVERRIDE = 2
STYLESHEET_APP = 3

class StyleSheet(Printer):
    def __init__(self, name: str, priority: int):
        super().__init__()
        self.name = name
        self.priority = priority

class BaseFramework:

    def __init__(self) -> None:
        # self.imports: list[tuple[str, str]] = []
        # self.effect_imports: list[str] = []
        self.styles = []

    def create(self, spec: AppSpec, artifact: Artifact):
        pass

    # def add_import(self, items: str, loc: str):
    #     self.imports.append((items, loc))

    # def add_effect_import(self, loc: str):
    #     self.effect_imports.append(loc)

    def add_style(self, name: str, priority: int):
        sheet = StyleSheet(name, priority)
        self.styles.append(sheet)
        return sheet

    def finalize(self, spec: AppSpec, artifact: Artifact):
        pass