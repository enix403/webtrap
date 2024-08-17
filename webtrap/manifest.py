import json
import requests

def npm_package_latest_version(name: str):
    url = f'https://registry.npmjs.org/{name}/latest'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        latest_version = data['version']
        return latest_version
    else:
        raise Exception(
            f"Error: Unable to fetch data for package '{name}'. "
            f"Status code: {response.status_code}"
        )

class PackageManifest:
    def __init__(self, name: str):
        self.name = name
        self.scripts: list[tuple[str, str]] = []
        self.deps: dict[str, str] = {}
        self.dev_deps: dict[str, str] = {}

    def add_script(self, name: str, command: str):
        self.scripts.append((name, command))

    def remove_script(self, name: str):
        for i, (script_name, _) in enumerate(self.scripts):
            if name == script_name:
                self.scripts.pop(i)
                break

    def add_dep(self, name: str, version: str):
        self.deps[name] = version

    def remove_dep(self, name: str):
        if name in self.deps:
            del self.deps[name]

    def add_dev_dep(self, name: str, version: str):
        self.dev_deps[name] = version

    def remove_dev_dep(self, name: str):
        if name in self.dev_deps:
            del self.dev_deps[name]

    def compile(self):
        data = {
            'name': self.name,
            'version': '1.0.0',
        }

        if len(self.scripts) > 0:
            data['scripts'] = dict(self.scripts)

        if len(self.deps) > 0:
            data['dependencies'] = dict(self.deps)

        if len(self.dev_deps) > 0:
            data['devDependencies'] = dict(self.dev_deps)

        return data

    def display(self):
        print(json.dumps(self.compile(), indent=2))