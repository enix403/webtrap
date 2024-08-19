from __future__ import annotations
from typing import TYPE_CHECKING

from webtrap.options import PrettierSpec

if TYPE_CHECKING:
    from webtrap.options import AppSpec, Artifact

def fill_prettier(spec: AppSpec, artifact: Artifact):
    assert spec.prettier is not None

    artifact.pkgjson.add_dev_dep('prettier', '^3.3.3')

    for p in spec.prettier.plugins:
        if p == PrettierSpec.PG_TAILWINDCSS:
            artifact.pkgjson.add_dev_dep(
                'prettier-plugin-tailwindcss',
                '^0.6.6'
            )