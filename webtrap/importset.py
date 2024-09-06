from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from webtrap.printers import JSPrinter

@dataclass
class Import:
    items: str
    location: str
    effect_only: bool

    def render(self) -> str:
        if self.effect_only:
            return f'import \"{self.location}\";'
        else:
            return f'import {self.items} from \"{self.location}\";'

    def render_to(self, printer: JSPrinter):
        if self.effect_only:
            printer.add_effect_import(self.location)
        else:
            printer.add_import(self.items, self.location)

class ImportSet:
    def __init__(self) -> None:
        self.imports: list[Import] = []

    def add(self, items: str, location: str):
        im = Import(items, location, False)
        self.imports.append(im)

    def add_effect(self, location: str):
        im = Import('', location, True)
        self.imports.append(im)

    def items(self) -> list[Import]:
        return self.imports
