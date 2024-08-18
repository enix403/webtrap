from fs import open_fs
from fs.memoryfs import MemoryFS
from fs.copy import copy_fs

from webtrap.options import AppSpec, Artifact
from webtrap.manifest import PackageManifest

def buildup(spec: AppSpec):
    fs = MemoryFS()
    pkgjson = PackageManifest('my-app')

    artifact = Artifact(fs, pkgjson)

    fr_fill_artifact(spec, artifact)

    with artifact.fs.open('package.json', 'w') as f:
        f.write(artifact.pkgjson.compile_str())

    with open_fs('generated') as target:
        target.removetree('/') # empty the directory
        copy_fs(artifact.fs, target)
        
        
def fr_fill_artifact(spec: AppSpec, artifact: Artifact):
    pass
