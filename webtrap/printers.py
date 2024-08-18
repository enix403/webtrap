import json
from typing import override

def get_indent(line: str):
    return len(line[:-len(line.lstrip())])

def pullback(content: str):
    lines = content.splitlines()

    min_indent = float('inf')

    for line in lines:
        if len(line.strip()) > 0:
            min_indent = min(
                get_indent(line),
                min_indent
            )

    for i in range(len(lines)):
        remove_indent = min(
            get_indent(lines[i]),
            min_indent
        )

        lines[i] = lines[i][remove_indent:]

    return '\n'.join(lines).strip() + '\n'

def indent_lines(content: str, indent=2):
    lines = content.splitlines()
    indent_str = ' ' * indent

    for i in range(len(lines)):
        lines[i] = indent_str + lines[i]

    return '\n'.join(lines).strip()

def wrap_indent(content: str, start: str, end: str, indent=2):
    return (
        start + '\n'
        + indent_lines(content, indent) + '\n'
        + end + '\n'
    )

class Printer:
    def __init__(self):
        self.buf = ''

    def get(self):
        return self.buf

    def add_line(self, line: str):
        self.buf += line + '\n'

    def add_chunk(self, chunk: str):
        self.buf += chunk

    def add_newline(self):
        self.add_line('')

    def add_pulled(self, content: str):
        self.add_chunk(pullback(content))

class JSFilePrinter(Printer):
    def add_import(self, items: str, loc: str):
        self.add_line(f'import {items} from \"{loc}\";')

    def add_effect_import(self, loc: str):
        self.add_line(f'import \"{loc}\";')


class ViteConfigPrinter(JSFilePrinter):
    def __init__(self):
        super().__init__()
        self.plugins: list[str] = []

        self.add_import("{ defineConfig }", "vite")

    def add_plugin(self, plugin: str, index: int | None = None):
        insert_index = len(self.plugins) if index is None else index
        self.plugins.insert(insert_index, plugin)

    def compile(self):
        return {
            'plugins': '[' + ',\n'.join(self.plugins) + ']',
            'define': {
                "process.env": {}
            },
            'server': {
                'port': 4200
            },
        }

    @override
    def get(self):
        configjson = json.dumps(self.compile(), indent=2)

        self.add_newline()
        self.add_pulled(f"""
            export default defineConfig({configjson});
        """)

        return super().get()