import re
from typing import Any, Iterable

def is_valid_js_identifier(key):
    return re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$', key) is not None

def py_to_js(obj: Any):
    if isinstance(obj, JSPrimitive):
        return obj
    elif isinstance(obj, str):
        return JSString(obj)
    elif isinstance(obj, (int, float)):
        return JSNumber(obj)
    elif isinstance(obj, (list, tuple, set)):
        return JSArray(obj)
    elif isinstance(obj, dict):
        return JSObject(obj)

    raise Exception("Unknown object")

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
    def __init__(self, values: Iterable[Any]):
        self.values = list(map(py_to_js, values))

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

class JSObject(JSPrimitive):
    def __init__(self, obj):
        properties = {}
        for key, val in obj.items():
            properties[key] = py_to_js(val)

        self.properties = properties

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
