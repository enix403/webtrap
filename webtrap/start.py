from beaupy import prompt
from caseconverter import kebabcase

from webtrap.appspec import AppSpec
from webtrap.features import framework as fr
from webtrap.features import langauge as ln
from webtrap.features import pkg_manager as pkm

from webtrap.common import select_enum
from webtrap.build import buildup

def input_spec():
    # Metadeta
    app_name = prompt("What is your app's name?")
    pkg_name = prompt(
        "What is your app's package name?",
        initial_value=kebabcase(app_name)
    )

    # Framework
    framework = select_enum(fr.Framework, 'Choose your framework:')
    # print(framework)

    # Language
    language = select_enum(ln.Langauge, 'Choose your langauge:')
    # print(lang)

    # Package Manager
    pkg_manager = select_enum(pkm.PackageManager, 'Choose your package manager:')
    # print(pkg_manager)

    spec = AppSpec(
        app_name=app_name,
        pkg_name=pkg_name,
        framework=framework,
        language=language,
        pkg_manager=pkg_manager,
    )

    return spec

def start():
    spec = input_spec()
    buildup(spec)



