def get_indent(line: str):
    return len(line[:-len(line.lstrip())])

def pullback(content: str):
    lines = content.splitlines()

    min_indent = -1

    for line in lines:
        if len(line.strip()) > 0:
            min_indent = get_indent(line)
            break

    # print(min_indent)
    if min_indent == -1:
        return content

    for i in range(len(lines)):
        remove_indent = min(
            get_indent(lines[i]),
            min_indent
        )

        lines[i] = lines[i][remove_indent:]

    return '\n'.join(lines).strip('\n').rstrip() + '\n'

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
        return self

    def add_chunk(self, chunk: str):
        self.buf += chunk
        return self

    def add_newline(self):
        self.add_line('')
        return self

    def add_pulled(self, content: str):
        self.add_chunk(pullback(content))
        return self

# ================================================

class JSPrinter(Printer):
    def __init__(self):
        super().__init__()
        self.has_imports = False

    def add_import(self, items: str, loc: str):
        self.add_line(f'import {items} from \"{loc}\";')
        self.has_imports = True
        return self

    def add_effect_import(self, loc: str):
        self.add_line(f'import \"{loc}\";')
        self.has_imports = True
        return self
