import shutil
from pathlib import Path

from fs import open_fs
from fs.memoryfs import MemoryFS
from fs.copy import copy_fs

from webtrap.features.langconfig import fill_langconfig
from webtrap.features.prettier import fill_prettier
from webtrap.features.tailwind import TailwindConfigPrinter, fill_tailwind

from webtrap.framework.react import ReactFramework
from webtrap.options import AppSpec, Artifact
from webtrap.manifest import PackageManifest

def buildup(spec: AppSpec, output_path: str):
    fs = MemoryFS()
    pkgjson = PackageManifest(spec.pkg_name)
    framework = ReactFramework()
    tailwindconf = TailwindConfigPrinter()

    artifact = Artifact(
        fs,
        pkgjson,
        framework,
        tailwindconf
    )

    # ======= fill the artifact =======

    framework.create(spec, artifact)

    fill_langconfig(spec, artifact)

    if spec.tw:
        fill_tailwind(spec, artifact)

    if spec.prettier:
        fill_prettier(spec, artifact)

    framework.finalize(spec, artifact)

    # ======= output the artifact =======

    with artifact.fs.open('package.json', 'w') as f:
        f.write(artifact.pkgjson.compile_str())

    if spec.tw:
        with artifact.fs.open(spec.language.file('tailwind.config'), 'w') as f:
            f.write(artifact.tailwindconf.get())

    dirpath = Path(output_path)

    if dirpath.is_dir():
        shutil.rmtree(dirpath)
    elif dirpath.is_file():
        dirpath.unlink()

    with open_fs(str(dirpath), create=True) as target:
        copy_fs(artifact.fs, target)
