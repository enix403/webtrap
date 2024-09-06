from webtrap.framework.react import ReactFramework
from webtrap.options import AppSpec, Artifact

def fill_routing(
    spec: AppSpec,
    artifact: Artifact
):
    fr = artifact.framework
    if isinstance(fr, ReactFramework):
        fr.entry_app_imports.add(
            '{ BrowserRouter, Route, Routes }',
            'react-router-dom'
        )
        artifact.pkgjson.add_dep("react-router-dom", '^6.26.1')

        # TODO: build tree
        fr.replace_entry_jsx("...")