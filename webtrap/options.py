from enum import Enum
from dataclasses import dataclass
from fs.memoryfs import MemoryFS

from webtrap.features.tailwind import TailwindConfigPrinter
from webtrap.framework.base import BaseFramework

from .manifest import PackageManifest


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
    
    def null_assert(self, expr: str):
        if self is self.Ts:
            return expr + "!"
        else:
            return expr

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

    def is_ts(self):
        return self.language is Langauge.Ts


@dataclass
class Artifact:
    fs: MemoryFS
    pkgjson: PackageManifest
    framework: BaseFramework
    # viteconf: ViteConfigPrinter
    tailwindconf: TailwindConfigPrinter
