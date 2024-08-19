from typing import override
from webtrap.jsobject import JSObject, JSRaw
from webtrap.printers import JSPrinter

class ViteConfigPrinter(JSPrinter):
    def __init__(self):
        super().__init__()
        self.plugins: list[str] = []
        self.add_import('{ defineConfig }', 'vite')

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