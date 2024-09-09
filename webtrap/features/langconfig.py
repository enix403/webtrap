from fs.copy import copy_file
from webtrap.options import AppSpec, Artifact, Framework, Langauge

def fill_langconfig(spec: AppSpec, artifact: Artifact):
    assert spec.framework is Framework.React

    source_path = "webtrap/skel/react"

    files: list[str]

    if spec.language is Langauge.Ts:        
        files = [
            "tsconfig.app.json",
            "tsconfig.node.json",
            "tsconfig.json",
        ]
    else:
        files = ['jsconfig.json']

    for file in files:
        copy_file(
            source_path,
            file,
            artifact.fs,
            file
        )