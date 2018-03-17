# Stdlib
import asyncio
import datetime

# Nano Core
from nano.core import route


class Registration:
    def __init__(self, nano):
        self.services = {}
        self._loop = True
        self._task = nano.loop.create_task(self.cleanup())

    def __del__(self):
        self._loop = False
        self._task.cancel()

    @property
    def service_names(self):
        return list(self.services.keys())

    async def cleanup(self):
        while self._loop:
            now = datetime.datetime.now().timestamp()
            new_services = {}
            for service_name, data in self.services:

                new_data = []
                for unit in data:
                    if now - unit["timestamp"] > 120:
                        new_data.append(unit)

                if new_data:
                    new_services[service_name] = new_data

            self.services = new_services
            await asyncio.sleep(10)

    @route("/registry/add_service", methods=["POST"])
    def register(self, request):
        time = round(datetime.datetime.now().timestamp())
        body = request.json
        srv_name = body["service_name"]
        ip = request.remote_addr

        data = {"address": ip, "timestamp": time}

        if srv_name in self.service_names:
            if ip in [d["address"] for d in self.service_names[srv_name]]:
                for d in self.service_names[srv_name]:
                    if d["address"] == ip:
                        d["timestamp"] = time

            else:
                self.services[srv_name].append(data)

        else:
            self.services[srv_name] = [data]
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
        ips = [x["address"] for x in self.services[srv_name]]
        return request.Response(code=200, json={"error": 0, "addresses": ips})

    @route("/registry/dump", methods=["GET"])
    def dump_all(self, request):
        return request.Response(code=200, json={"error": 0, "data": self.services})


def setup(nano):
    nano.add_route_cog(Registration(nano))
