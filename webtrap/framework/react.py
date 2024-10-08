from fs import open_fs
from fs.copy import copy_file
from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape


from webtrap.common import load_skel_jinja
from webtrap.options import AppSpec, Artifact, Framework, Langauge
from webtrap.printers import (
    Printer,
    JSPrinter,
    pullback,
)

from webtrap.framework.base import BaseFramework
from .vite import ViteConfigPrinter

from webtrap.importset import ImportSet

class ReactFramework(BaseFramework):
    def __init__(self):
        super().__init__()
        self.entry_app_imports = ImportSet()

    def create(self, spec: AppSpec, artifact: Artifact):

        artifact.pkgjson.add_extra('type', 'module')

        artifact.pkgjson.add_dep('react', '^18.3.1')
        artifact.pkgjson.add_dep('react-dom', '^18.3.1')

        artifact.pkgjson.add_dev_dep("@types/react", "^18.3.3")
        artifact.pkgjson.add_dev_dep("@types/react-dom", "^18.3.0")
        artifact.pkgjson.add_dev_dep("@vitejs/plugin-react", "^4.3.1")
        artifact.pkgjson.add_dev_dep("vite", "^5.4.1")
        if spec.language is Langauge.Ts:
            artifact.pkgjson.add_dev_dep("typescript", "^5.5.3")

        artifact.pkgjson.add_script("dev", "vite")
        if spec.language is Langauge.Ts:
            artifact.pkgjson.add_script("build", "tsc -b && vite build")
            artifact.pkgjson.add_script("typecheck", "tsc --noEmit")
        else:
            artifact.pkgjson.add_script("build", "vite build")
        artifact.pkgjson.add_script("preview", "vite preview")

        if spec.routing:
            artifact.pkgjson.add_dep("react-router-dom", '^6.26.1')


        viteconf = ViteConfigPrinter()
        viteconf.add_import("react", "@vitejs/plugin-react")
        viteconf.add_plugin("react()")

        if spec.language is Langauge.Ts:
            artifact.pkgjson.add_dev_dep("vite-tsconfig-paths", '^5.0.1')
            viteconf.add_import("tsconfigPaths", "vite-tsconfig-paths")
            viteconf.add_plugin("tsconfigPaths()")
        else:
            artifact.pkgjson.add_dev_dep("vite-jsconfig-paths", '^2.0.1')
            viteconf.add_import("jsconfigPaths", "vite-jsconfig-paths")
            viteconf.add_plugin("jsconfigPaths()")

        with artifact.fs.open(spec.language.file('vite.config'), 'w') as f:
            f.write(viteconf.get())

        self.root_fs = artifact.fs
        self.src_fs = artifact.fs.makedir("src")
        self.styles_fs = artifact.fs.makedirs('src/styles')

        artifact.fs.makedirs('src/components')
        artifact.fs.makedirs('public')

        self.add_files(spec)

        if spec.is_ts():
            self.src_fs.writetext("vite-env.d.ts", pullback("""
                /// <reference types="vite/client" />
            """))

    def finalize(self, spec: AppSpec, artifact: Artifact):
        src = self.src_fs

        mainfile_name = spec.language.file_jsx("main")
        with src.open(mainfile_name, 'w') as f:
            p = JSPrinter()

            p.add_import("{ createRoot }", 'react-dom/client')
            p.add_import("{ App }", './App')

            p.add_newline()

            p.add_pulled(f"""
            const root = document.getElementById('root');
            createRoot({spec.language.null_assert("root")}).render(<App />);
            """)
            f.write(p.get())

        sorted_styles = sorted(self.styles, key=lambda style: style.priority)

        for stylesheet in sorted_styles:
            self.styles_fs.writetext(stylesheet.name, stylesheet.get())

        with src.open(spec.language.file_jsx("App"), 'w') as f:
            p = JSPrinter()
            
            for stylesheet in sorted_styles:
                p.add_effect_import('./styles/' + stylesheet.name)

            if sorted_styles:
                p.add_newline()

            for im in self.entry_app_imports.items():
                im.render_to(p)

            p.add_line(
                load_skel_jinja("react/App.jsx.jinja")
                    .render(spec=spec)
            )

            f.write(p.get())

        with artifact.fs.open("index.html", 'w') as f:
            p = Printer()
            p.add_pulled(f"""
            <!DOCTYPE HTML>
            <html lang="en">
              <head>
                <meta charset="UTF-8" />
                <link rel="icon" type="image/svg+xml" href="/vite.svg" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <title>{spec.app_name}</title>
              </head>
              <body>
                <div id="root"></div>
                <script type="module" src="/src/{mainfile_name}"></script>
              </body>
            </html>
            """)
            f.write(p.get())

    def add_files(self, spec: AppSpec):
        with open_fs('webtrap/skel/react') as src_fs:
            file = "components/" + spec.language.file_jsx('loadable')
            copy_file(src_fs, file, self.src_fs, file)

            copy_file(src_fs, '.gitignore', self.root_fs, '.gitignore')

            with self.root_fs.open('README.md', 'w') as readme_f:
                readme_f.write(
                    load_skel_jinja("react/README.md.jinja")
                        .render(app_name=spec.app_name)
                )
