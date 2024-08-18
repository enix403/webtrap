def get_indent(line: str):
    return len(line[:-len(line.lstrip())])

def pullback(content: str):
    lines = content.split('\n')

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

    return '\n'.join(lines).strip()

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
        self.add_line(f'import {items} from \"{loc}\"')

    def add_effect_import(self, loc: str):
        self.add_line(f'import \"{loc}\"')