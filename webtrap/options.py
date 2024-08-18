from enum import Enum
from dataclasses import dataclass

from .manifest import PackageManifest
from fs.memoryfs import MemoryFS

class Framework(Enum):
    React = 'React'
    Remix = 'Remix'
    Next = 'Next'
    Svelte = 'Svelte'
    SvelteKit = 'SvelteKit'
    Astro = 'Astro'

class Langauge(Enum):
    Js = 'JavaScript'
    Ts = 'TypeScript'

class PackageManager(Enum):
    Pnpm = 'pnpm'
    Yarn = 'yarn'
    Npm = 'npm'


@dataclass
class AppSpec:
    app_name: str
    pkg_name: str
    framework: Framework
    language: Langauge
    pkg_manager: PackageManager


@dataclass
class Artifact:
    fs: MemoryFS
    pkgjson: PackageManifest
