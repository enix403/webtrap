from beaupy import prompt
from caseconverter import kebabcase

from webtrap.options import AppSpec
from webtrap.options import Framework
from webtrap.options import Langauge
from webtrap.options import PackageManager

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
    framework = select_enum(Framework, 'Choose your framework:')
    # print(framework)

    # Language
    language = select_enum(Langauge, 'Choose your langauge:')
    # print(lang)

    # Package Manager
    pkg_manager = select_enum(PackageManager, 'Choose your package manager:')
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
    spec = AppSpec(
        app_name="Dummy App",
        pkg_name="dummy-app",
        framework=Framework.React,
        language=Langauge.Ts,
        pkg_manager=PackageManager.Pnpm
    )
    spec = input_spec()

    output_path = "generated/react"

    buildup(spec, output_path)



