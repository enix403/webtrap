from fs import open_fs
from fs.memoryfs import MemoryFS
from fs.copy import copy_fs

from webtrap.options import AppSpec, Artifact, Framework
from webtrap.manifest import PackageManifest
from webtrap.printers import JSFilePrinter

def buildup(spec: AppSpec):
    fs = MemoryFS()
    pkgjson = PackageManifest('my-app')

    artifact = Artifact(fs, pkgjson)

    fill_framework(spec, artifact)

    with artifact.fs.open('package.json', 'w') as f:
        f.write(artifact.pkgjson.compile_str())

    with open_fs('generated') as target:
        target.removetree('/') # empty the directory
        copy_fs(artifact.fs, target)

def fill_framework(spec: AppSpec, artifact: Artifact):
    assert(spec.framework is Framework.React)

    artifact.fs.makedir("src")
    src = artifact.fs.opendir('src')

    with src.open(spec.language.file_jsx("main"), 'w') as f:
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
