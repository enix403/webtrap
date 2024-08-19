from webtrap.options import AppSpec, Artifact, Framework, Langauge
from webtrap.printers import (
    Printer,
    JSPrinter,
    pullback,
)

from webtrap.framework.base import BaseFramework
from .vite import ViteConfigPrinter


class ReactFramework(BaseFramework):
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


        viteconf = ViteConfigPrinter()
        viteconf.add_import("react", "@vitejs/plugin-react")
        viteconf.add_plugin("react()")

        with artifact.fs.open(spec.language.file('vite.config'), 'w') as f:
            f.write(viteconf.get())

        self.src_fs = artifact.fs.makedir("src")
        self.styles_fs = artifact.fs.makedirs('src/styles')

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

            p.add_pulled("""
            export function App() {
              return (
                <>
                  <h1>React App</h1>
                  <div>
                    Hello there
                  </div>
                </>
              );
            }
            """)
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