import shutil, psutil, logging, os
class DiskDetector:
    
    def detect(self, yaml_config, disk_data):
        inode_threshold = yaml_config["inode_exhaustion_warning_threshold"]
        print("disk data", disk_data)

