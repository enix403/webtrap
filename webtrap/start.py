from dataclasses import dataclass
from beaupy import prompt
from caseconverter import kebabcase

from webtrap.features import framework as fr
from webtrap.features import langauge as ln
from webtrap.features import pkg_manager as pkm

from webtrap.common import select_enum
from webtrap.build import buildup

def start():
    pass

    buildup()

    # Metadeta
    # app_name = prompt("What is your app's name?")
    # package_name = prompt(
    #     "What is your app's package name?",
    #     initial_value=kebabcase(app_name)
    # )

    # Framework
    # framework = select_enum(fr.Framework, 'Choose your framework:')
    # print(framework)

    # Language
    # lang = select_enum(ln.Langauge, 'Choose your langauge:')
    # print(lang)

    # Package Manager
    # pkg_manager = select_enum(pkm.PackageManager, 'Choose your package manager:')
    # print(pkg_manager)

