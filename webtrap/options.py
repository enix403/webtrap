from __future__ import annotations

from enum import Enum
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
from fs.memoryfs import MemoryFS

if TYPE_CHECKING:
    from .features.tailwind import TailwindConfigPrinter
    from .framework.base import BaseFramework
    from .manifest import PackageManifest


class Framework(Enum):
    React = 'React'
    Remix = 'Remix'
    Next = 'Next'
    Svelte = 'Svelte'
    SvelteKit = 'SvelteKit'
    Astro = 'Astro'

class Langauge(Enum):
    Ts = 'TypeScript'
    Js = 'JavaScript'

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

class TailwindSpec:
    PG_BREAKPOINTS_INSPECTOR = 'tailwindcss-breakpoints-inspector'
    PG_RIPPLE_UI = 'rippleui'

    def __init__(self, plugins: list[str]) -> None:
        self.plugins = plugins

    @classmethod
    def get_available_plugins(cls):
        return [
            cls.PG_BREAKPOINTS_INSPECTOR,
            cls.PG_RIPPLE_UI
        ]

class PrettierSpec:
    PG_TAILWINDCSS = 'prettier-plugin-tailwindcss'

    def __init__(self, plugins: list[str]) -> None:
        self.plugins = plugins

    @classmethod
    def get_available_plugins(cls, tw_spec: Optional[TailwindSpec]):
        return [
            cls.PG_TAILWINDCSS
        ] if tw_spec else []

available_other_libs: list[str] = [
    'clsx',
    'react-helmet',
    '@tabler/icons-react',
    '@heroicons/react',
    '@phosphor-icons/react',
    'axios',
    'date-fns',
    'immer',
    'framer-motion',
    'react-html-props',
    'ts-pattern',
] 

@dataclass
class AppSpec:
    app_name: str
    pkg_name: str
    framework: Framework
    language: Langauge
    pkg_manager: PackageManager
    tw: Optional[TailwindSpec]
    prettier: Optional[PrettierSpec]
    routing: bool
    other_libs: list[str]

    def is_ts(self):
        return self.language is Langauge.Ts


@dataclass
class Artifact:
    fs: MemoryFS
    pkgjson: PackageManifest
    framework: BaseFramework
    tailwindconf: TailwindConfigPrinter
