from __future__ import annotations
from typing import TYPE_CHECKING, Any
import json

from fs import open_fs
from fs.copy import copy_file

from webtrap.options import PrettierSpec

if TYPE_CHECKING:
    from webtrap.options import AppSpec, Artifact

def fill_prettier(spec: AppSpec, artifact: Artifact):
    assert spec.prettier is not None

    artifact.pkgjson.add_dev_dep('prettier', '^3.3.3')

    artifact.pkgjson.add_script(
        "format",
        "prettier -uw --cache --ignore-path .prettierignore ."
    )

    plugins = []

    for p in spec.prettier.plugins:
        if p == PrettierSpec.PG_TAILWINDCSS:
            artifact.pkgjson.add_dev_dep(
                'prettier-plugin-tailwindcss',
                '^0.6.6'
            )
            plugins.append(p)

    skel_path = "webtrap/skel/prettier"
    skel_fs = open_fs(skel_path)

    copy_file(skel_fs, '.prettierignore', artifact.fs, '.prettierignore')

    config: dict[str, Any] = {}
    with skel_fs.open('.prettierrc.json') as f:
        config = json.load(f)
        if plugins:
            config['plugins'] = plugins

    artifact.fs.writetext('.prettierrc.json', json.dumps(
        config,
        indent=2
    ))


