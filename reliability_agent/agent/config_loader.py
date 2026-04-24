import yaml, os, logging
import pathlib as Path


class ConfigLoader:
    def __init__(self, config_path):
        self.config_path = config_path
        if config_path is None:
            self.config_path = os.getenv("./reliability_agent/configs/agent.yaml", "./reliability_agent/configs/default.yaml") # Getting agent config, if not there default to default
    
    def load_config(self):
        with open(self.config_path, 'r') as config:
            print(yaml.safe_load(config))
            return yaml.safe_load(config)