import re
from typing import Any

# Utility function to check if a string is a valid JavaScript identifier
def is_valid_js_identifier(key):
    return re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$', key) is not None

class JSPrimitive:
    def output(self, indent=2, curr_indent=0):
        raise NotImplementedError()

class JSNumber(JSPrimitive):
    def __init__(self, value):
        self.value = value

    def output(self, indent=2, curr_indent=0):
        return str(self.value)

class JSString(JSPrimitive):
    def __init__(self, value):
        self.value = value

    def output(self, indent=2, curr_indent=0):
        return f'"{self.value}"'

class JSRaw(JSPrimitive):
    def __init__(self, value):
        self.value = value

    def output(self, indent=2, curr_indent=0):
        return self.value

class JSArray(JSPrimitive):
    def __init__(self, values: list[JSPrimitive]):
        self.values = values

    def output(self, indent=2, curr_indent=0):
        if len(self.values) == 0:
            return '[]'

        curr_indent_str = ' ' * curr_indent

        next_indent = curr_indent + indent;
        next_indent_str = ' ' * next_indent

        elements = [
            f"{next_indent_str}{value.output(indent, next_indent)}"
            for value in self.values
        ]
        return f'[\n{",\n".join(elements)}\n{curr_indent_str}]'

class JSObject:
    def __init__(self, **kwargs):
        self.properties = kwargs

    def output(self, indent=2, curr_indent=0):
        if len(self.properties) == 0:
            return '{}'

        curr_indent_str = ' ' * curr_indent

        next_indent = curr_indent + indent;
        next_indent_str = ' ' * next_indent

        items = []
        for key, value in self.properties.items():
            js_key = key if is_valid_js_identifier(key) else f'"{key}"'
            items.append(
                f'{next_indent_str}{js_key}: {value.output(indent, next_indent)}'
            )

        return f'{{\n{",\n".join(items)}\n{curr_indent_str}}}'
