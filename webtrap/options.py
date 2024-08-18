from enum import Enum
from dataclasses import dataclass
from fs.memoryfs import MemoryFS


from .manifest import PackageManifest
from .printers import ViteConfigPrinter

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

    def file(self, name: str):
        ext = "js" if self is self.Js else 'ts'
        return f'{name}.{ext}'

    def file_jsx(self, name: str):
        ext = "jsx" if self is self.Js else 'tsx'
        return f'{name}.{ext}'

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
    viteconf: ViteConfigPrinter