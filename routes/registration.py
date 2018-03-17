# Nano Core
from nano.core import route


class Registration:
    def __init__(self):
        self.services = {}
        self.service_names = []

    @route("/registry/add_service", methods=["POST"])
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

    @route("/registry/get_service", methods=["GET"])
    def get_registered(self, request):
        body = request.query
        srv_name = body["service_name"]
        ips = self.services[srv_name]
        return request.Response(code=200, json={"error": 0, "addresses": ips})

    @route("/registry/dump", methods=["GET"])
    def dump_all(self, request):
        return request.Response(code=200, json={"error": 0, "data": self.services})


def setup(nano):
    nano.add_route_cog(Registration())
