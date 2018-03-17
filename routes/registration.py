# Nano Core
from nano.core import route


class Registration:
    def __init__(self):
        self.services = {}
        self.service_names = []

    @route("/registry/add_service", methods="POST")
    def register(self, request):
        body = request.json
        srv_name = body["service_name"]
        ip = request.remote_addr
        if srv_name in self.service_names:
            self.services[srv_name].append(ip)

        else:
            self.services[srv_name] = [ip]
            self.service_names.append(srv_name)

        return request.Response(
            code=200, json={
                "error": 0,
                "message": "Service registration success."
            })


def setup(nano):
    nano.add_route_cog(Registration())
