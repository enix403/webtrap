from dataclasses import dataclass

from webtrap.manifest import PackageManifest
from .features.framework import Framework
from .features.langauge import Langauge

from fs import open_fs
from fs.memoryfs import MemoryFS
from fs.copy import copy_fs

@dataclass
class AppSpec:
    framework: Framework
    language: Langauge

@dataclass
class Artifact:
    fs: MemoryFS
    pkgjson: PackageManifest

def buildup():
    fs = MemoryFS()
    pkgjson = PackageManifest('my-app')

    artifact = Artifact(fs, pkgjson)

    # fs.makedir('src')

    with artifact.fs.open('package.json', 'w') as f:
        f.write(artifact.pkgjson.compile_str())

    with open_fs('generated') as target:
        target.removetree('/') # empty the directory
        copy_fs(artifact.fs, target)