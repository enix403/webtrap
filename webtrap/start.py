from dataclasses import dataclass
from beaupy import prompt
from caseconverter import kebabcase

from webtrap.features import framework as fr
from webtrap.features import langauge as ln
from webtrap.features import pkg_manager as pkm

# @dataclass
# class AppSpec:
#     pkg_manager: PackageManager
#     framework: Framework

def start():
    # Metadeta
    # app_name = prompt("What is your app's name?")
    # package_name = prompt(
    #     "What is your app's package name?",
    #     initial_value=kebabcase(app_name)
    # )

    # Framework
    # framework = fr.ask()
    # print(framework)

    # Language
    lang = ln.ask()
    print(lang)

