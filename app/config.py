import yaml
from os import path


class Config():

    def __init__(self):
        pass

    def return_config(self):
        config_path = path.relpath("config/config.yaml")
        config = yaml.load(open(config_path))
        server = config["server"]
        port = config["port"]
        channel = config["channel"]
        nickname = config["nickname"]
        prompt = config["prompt"]
        return {"server": server, "port": port, "channel": channel,
                "nickname": nickname, "prompt": prompt}
