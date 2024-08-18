from enum import Enum

from webtrap.appspec import AppSpec, Artifact

class Framework(Enum):
    React = 'React'
    Remix = 'Remix'
    Next = 'Next'
    Svelte = 'Svelte'
    SvelteKit = 'SvelteKit'
    Astro = 'Astro'


def fr_fill_artifact(spec: AppSpec, artifact: Artifact):
    assert spec.framework is Framework.React