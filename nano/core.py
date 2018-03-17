# Stdlib
import importlib
import inspect

# External Libraries
from japronto import Application


def route(*args, **kwargs):
    def decorator(func):
        return Route(func, *args, **kwargs)

    return decorator


class Route:
    def __init__(self, func, path, methods, *args, **kwargs):
        self.func = func
        self.path = path
        self.methods = methods
        self.args = args
        self.kwargs = kwargs

    def run(self, request):
        return self.func(request)


class Nano(Application):
    def __init__(self, address, port, *args, **kwargs):
        self.address = address
        self.port = port
        super().__init__()

    def load_ext(self, import_path):
        lib = importlib.import_module(import_path)
        lib.setup(self)
        del lib

    def add_route_cog(self, cog):
        for func in inspect.getmembers(cog):
            if isinstance(func, Route):
                self.router.add_route(
                    func.path, func.run, methods=func.methods, *func.args, **func.kwargs)

    def start(self):
        self.run((self.address, self.port))
