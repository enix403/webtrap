from __future__ import annotations
from typing import TYPE_CHECKING

from fs import open_fs
from fs.copy import copy_file

if TYPE_CHECKING:
    from webtrap.options import AppSpec, Artifact

def fill_vercel(spec: AppSpec, artifact: Artifact):
    assert spec.add_vercel_json

    skel_path = "webtrap/skel/vercel"
    skel_fs = open_fs(skel_path)

    copy_file(skel_fs, 'vercel.json', artifact.fs, 'vercel.json')