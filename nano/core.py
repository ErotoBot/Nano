# Stdlib
import importlib
import inspect

# External Libraries
from japronto import Application, RouteNotFoundException


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

    def set_cog(self, cog):
        self.cog = cog

    def run(self, req):
        if hasattr(self, "cog"):
            return self.func(self.cog, req)
        return self.func(req)


class Nano(Application):
    def __init__(self, address, port, *args, **kwargs):
        self.address = address
        self.port = port
        super().__init__()
        self.add_error_handler(KeyError, self.KeyErrorHandler)
        self.add_error_handler(RouteNotFoundException, self.NotFoundHandler)

    @staticmethod
    def KeyErrorHandler(req, err):
        return req.Response(
            code=400, json={
                "error": 400,
                "message": f"Invalid data, mising key: {err.args[0]!r}"
            })

    @staticmethod
    def NotFoundHandler(req, _err):
        return req.Response(code=404, json={"error": 404, "message": "Not Found"})

    def load_ext(self, import_path):
        lib = importlib.import_module(import_path)
        lib.setup(self)
        del lib

    def add_route_cog(self, cog):
        print("==", cog.__class__.__name__, "==")
        for name, func in inspect.getmembers(cog):
            if isinstance(func, Route):
                func.set_cog(cog)
                print("Adding route")
                print(func.path)
                self.router.add_route(
                    func.path, func.run, methods=func.methods, *func.args, **func.kwargs)

    def start(self):
        self.run(self.address, self.port, debug=True)
