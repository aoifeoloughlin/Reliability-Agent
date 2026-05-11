import yaml, os, logging
import pathlib as Path

class ConfigLoader:
    def __init__(self, config_path):
        print(config_path)
        self.config_path = config_path
        if config_path is None:
            self.config_path = "../reliability_agent/configs/default.yaml" # Getting agent config, if not there default to default
    
    def load_config(self):
        try:
            with open(self.config_path, 'r') as config:
                config_yaml = yaml.safe_load(config)
            return config_yaml
        except Exception as e:
            print("ERROR:", e)
            traceback.print_exc()