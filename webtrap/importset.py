from dataclasses import dataclass

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

class ImportSet:
    def __init__(self) -> None:
        self.imports: list[Import] = []

    def add(self, items: str, location: str):
        im = Import(items, location, False)
        self.imports.append(im)

    def add_effect(self, location: str):
        im = Import('', location, True)
        self.imports.append(im)
