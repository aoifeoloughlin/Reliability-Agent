import shutil, psutil, logging, os, json
class DiskDetector:
    
    def detect(self, yaml_config, disk_data):
        inode_warning_threshold = yaml_config["inode_exhaustion_warning_threshold"]
        inode_critical_threshold = yaml_config["inode_exhaustion_critical_threshold"]
        disk = json.loads(disk_data)
        inode_perc = disk[0]["inode_perc"]

        if inode_perc < inode_threshold:
            disk_usage_level = "NORMAL"
        else if inode_perc < inode_warning_threshold and inode_perc > inode_critical_threshold:
            disk_usage_level = "WARNING"
        else:
            disk_usage_level = "CRITICAL"

        return disk_usage_level

