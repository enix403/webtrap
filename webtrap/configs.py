class ViteConfig:
    def __init__(self):
        self.plugins: list[str] = []

    def add_plugin(self, plugin: str, index: int | None = None):
        insert_index = len(self.plugins) if index is None else index
        self.plugins.insert(insert_index, plugin)

    def compile(self):
        return {
            'plugins': self.plugins.copy(),
            'define': {
                "process.env": {}
            },
            'server': {
                'port': 4200
            },
        }