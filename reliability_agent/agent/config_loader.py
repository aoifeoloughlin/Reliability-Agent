import yaml, os
import pathlib as Path

class ConfigLoader:
    def __init__(self, config_name=None):
        self.config_name = config_name
        if config_name is None:
            self.config_name = os.getenv("agent", "default") # Getting agent config, if not there default to default

        self.config_path = (
            Path(__file__).resolve().parent.parent 
        )
    
    def load_config(self):
        with open(self.config_path) as config:
            return yaml.safe_load(config)