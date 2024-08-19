from __future__ import annotations
from typing import TYPE_CHECKING, override
from webtrap.framework.base import STYLESHEET_APP, STYLESHEET_RESET
from webtrap.jsobject import JSObject, JSRaw
from webtrap.printers import JSPrinter

if TYPE_CHECKING:
    from webtrap.options import AppSpec, Artifact

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

        if self.has_imports:
            self.add_newline()

        self.add_pulled(f"""
        /** @type {{import('tailwindcss').Config}} */
        export default {js_object};
        """)

        return super().get()


def fill_tailwind(spec: AppSpec, artifact: Artifact):
    artifact.pkgjson.add_dev_dep('tailwindcss', '^3.3.3')
    artifact.pkgjson.add_dev_dep('postcss', '^8.4.38')
    artifact.pkgjson.add_dev_dep('autoprefixer', '^10.4.15')

    artifact.tailwindconf.add_content("./index.html")
    artifact.tailwindconf.add_content("./src/**/*.{js,ts,jsx,tsx}")

    with artifact.fs.open('postcss.config.js', 'w') as f:
        p = JSPrinter()
        p.add_pulled("""
        export default {
          plugins: {
            tailwindcss: {},
            autoprefixer: {},
          }
        };
        """)
        f.write(p.get())


    reset = artifact.framework.add_style('tailwind-reset.css', STYLESHEET_RESET)
    reset.add_pulled("""
    @tailwind base;
    """)

    content = artifact.framework.add_style('tailwind-content.css', STYLESHEET_APP)
    content.add_pulled("""
    @tailwind components;
    @tailwind utilities;
    """)
