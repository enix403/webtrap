import shutil
from pathlib import Path

from fs import open_fs
from fs.memoryfs import MemoryFS
from fs.copy import copy_fs


from webtrap.options import AppSpec, Artifact, Framework, Langauge
from webtrap.manifest import PackageManifest
from webtrap.printers import (
    Printer,
    JSFilePrinter,
    ViteConfigPrinter,
)

def buildup(spec: AppSpec, output_path: str):
    fs = MemoryFS()
    pkgjson = PackageManifest('my-app')
    viteconf = ViteConfigPrinter()

    artifact = Artifact(
        fs,
        pkgjson,
        viteconf
    )

    fill_framework(spec, artifact)

    with artifact.fs.open('package.json', 'w') as f:
        f.write(artifact.pkgjson.compile_str())

    with artifact.fs.open(spec.language.file('vite.config'), 'w') as f:
        f.write(artifact.viteconf.get())

    dirpath = Path(output_path)

    if dirpath.is_dir():
        shutil.rmtree(dirpath)
    elif dirpath.is_file():
        dirpath.unlink()

    with open_fs(str(dirpath), create=True) as target:
        copy_fs(artifact.fs, target)

# ----------------------------------------------
# ----------------------------------------------
# ----------------------------------------------
# ----------------------------------------------
# ----------------------------------------------

def fill_framework(spec: AppSpec, artifact: Artifact):
    assert(spec.framework is Framework.React)

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
    else:
        artifact.pkgjson.add_script("build", "vite build")
    artifact.pkgjson.add_script("preview", "vite preview")


    artifact.viteconf.add_import("react", "@vitejs/plugin-react")
    artifact.viteconf.add_plugin("react()")


    artifact.fs.makedir("src")
    src = artifact.fs.opendir('src')

    mainfile_name = spec.language.file_jsx("main")
    with src.open(mainfile_name, 'w') as f:
        p = JSFilePrinter()

        p.add_import("{ createRoot }", 'react-dom/client')
        p.add_import("{ App }", './App')

        p.add_newline()

        p.add_pulled("""
        const root = document.getElementById('root');
        createRoot(root).render(<App />);
        """)
        f.write(p.get())

    with src.open(spec.language.file_jsx("App"), 'w') as f:
        p = JSFilePrinter()
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


def fill_tsconfig(spec: AppSpec, artifact: Artifact):
    pass