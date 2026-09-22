import shutil, psutil, logging
class DiskCollector:
    def __init__(self):
        self.usage_stats = []
        
    def collect(self):
        for partition in psutil.disk_partitions(all=True):
            if partition.mountpoint != '/': # the code trys to get the partition with the root
                continue
            try:
                usage = psutil.disk_usage('/')
                self.usage_stats.append({
                    "device": partition.device,
                    "mount_point": partition.mountpoint,
                    "usage_percent": usage.percent,
                })
            except PermissionError:
                logging.warning(
                    "Permission denied accessing %s",
                    partition.mountpoint,
                )
                continue
            except Exception as e:
                logging.warning(
                    "Failed to collect usage for %s: %s",
                    partition.mountpoint,
                    e,
                )
                continue
        return self.usage_stats
        