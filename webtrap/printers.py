from typing import Any, override

from webtrap.jsobject import JSArray, JSNumber, JSObject, JSRaw

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

# ================================================

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

# ================================================

class JSPrinter(Printer):
    def __init__(self):
        super().__init__()
        self.has_imports = False

    def add_import(self, items: str, loc: str):
        self.add_line(f'import {items} from \"{loc}\";')
        self.has_imports = True

    def add_effect_import(self, loc: str):
        self.add_line(f'import \"{loc}\";')
        self.has_imports = True

# ================================================

class ViteConfigPrinter(JSPrinter):
    def __init__(self):
        super().__init__()
        self.plugins: list[str] = []

    def add_plugin(self, plugin: str, index: int | None = None):
        insert_index = len(self.plugins) if index is None else index
        self.plugins.insert(insert_index, plugin)

    def compile(self) -> JSObject:
        return JSObject({
            'plugins': [JSRaw(p) for p in self.plugins],
            'define': {
                'process.env': {}
            },
            'server': {
                'port': 4200
            }
        })

    @override
    def get(self):
        js_object = self.compile().output(2)

        self.add_newline()
        self.add_pulled(f"""
            export default defineConfig({js_object});
        """)

        return super().get()

# ================================================

class TailwindConfigPrinter(JSPrinter):
    def __init__(self):
        super().__init__()
        self.content: list[str] = []
        self.plugins: list[str] = []

    def add_content(self, item: str):
        self.content.append(item)

    def add_plugin(self, plugin: str, index: int | None = None):
        insert_index = len(self.plugins) if index is None else index
        self.plugins.insert(insert_index, plugin)

    def compile(self) -> JSObject:
        return JSObject({
            'content': self.content,
            'plugins': [JSRaw(p) for p in self.plugins],
        })

    @override
    def get(self):
        js_object = self.compile().output(2)

        # if self.has_imports:
        # self.add_newline()

        self.add_pulled(f"""
            /** @type {{import('tailwindcss').Config}} */
            export default {js_object};
        """)

        return super().get()

