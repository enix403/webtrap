from beaupy import confirm, prompt, select_multiple
from caseconverter import kebabcase

from webtrap.options import AppSpec, PrettierSpec, TailwindSpec
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

    # Tailwind
    tw_spec: TailwindSpec | None = None

    tw_enabled = bool(confirm("Do you want to add tailwind?", default_is_yes=True))
    if tw_enabled:
        print("Choose any tailwind plugins you want:")
        selected_plugins: list[str] = select_multiple(
            TailwindSpec.get_available_plugins()
        )
        
        tw_spec = TailwindSpec(selected_plugins)

    # Prettier
    pt_spec: PrettierSpec | None = None

    pt_enabled = bool(confirm("Do you want to add prettier?", default_is_yes=True))
    if pt_enabled:
        available = PrettierSpec.get_available_plugins(tw_spec)
        selected_plugins: list[str] = []

        if available:
            print("Choose any prettier plugins you want:")
            selected_plugins: list[str] = select_multiple(available)

        pt_spec = PrettierSpec(selected_plugins)

    # Combine all inputs
    spec = AppSpec(
        app_name=app_name,
        pkg_name=pkg_name,
        framework=framework,
        language=language,
        pkg_manager=pkg_manager,
        tw=tw_spec,
        prettier=pt_spec
    )

    return spec

def start():
    spec = AppSpec(
        app_name="Dummy App",
        pkg_name="dummy-app",
        framework=Framework.React,
        language=Langauge.Ts,
        pkg_manager=PackageManager.Pnpm,
        tw=TailwindSpec([TailwindSpec.PG_BREAKPOINTS_INSPECTOR, TailwindSpec.PG_RIPPLE_UI]),
        prettier=PrettierSpec([PrettierSpec.PG_TAILWINDCSS])
    )
    spec = input_spec()

    output_path = "generated/react"

    buildup(spec, output_path)



