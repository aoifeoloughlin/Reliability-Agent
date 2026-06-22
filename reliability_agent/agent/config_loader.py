import yaml, os, logging
import pathlib as Path
from agent.logging_content from get_logger

class ConfigLoader:
    def __init__(self, config_path):
        print(config_path)
        self.config_path = config_path
        if config_path is None:
            self.config_path = "../reliability_agent/configs/default.yaml" # Getting agent config, if not there default to default
    
    logger = get_logger()

    def load_config(self):
        try:
            with open(self.config_path, 'r') as config:
                config_yaml = yaml.safe_load(config)
                logger.info("Config loaded successfully", extra={"config_yaml":config_yaml})
            return config_yaml
        except Exception as e:
            logger.ERROR("ERROR:", e)
            traceback.print_exc()