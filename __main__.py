# Nano Core
from nano.core import Nano
import ujson as json

with open("config.json") as f:
    CONFIG = json.load(f)

ADDRESS = ("0.0.0.0", CONFIG.get("port", 4080))  # noqa: B104

nano = Nano(*ADDRESS)

for path in CONFIG["paths"]:
    nano.load_ext(path)

nano.start()
