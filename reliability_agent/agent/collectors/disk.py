import shutil, logging, psutil
class DiskCollector:
    def __init__(self):
        self.PSEUDO_FILESYSTEMS = {
            "proc",
            "sysfs",
            "tmpfs",
            "devtmpfs",
            "devpts",
            "cgroup",
            "cgroup2",
            "securityfs",
            "tracefs",
            "overlay",
            "squashfs",
            "mqueue",
            "debugfs",
            "pstore",
            "configfs",
            "fusectl",
        }
        self.usage_stats = []

    def collect(self):
        try:
            partitions = psutil.disk_partitions(all=False)
        except Exception as e:
            logging.error("Failed to retrieve disk partitions: %s", e)
            return []
        return self.get_usage_metrics(partitions)
        
    def get_usage_metrics(self, partitions):
        for partition in partitions:
            if partition.fstype in self.PSEUDO_FILESYSTEMS:
                continue
            
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                self.usage_stats.append({
                    "filesystem": partition.device,
                    "mount_point": partition.mountpoint,
                    "filesystem_type": partition.fstype,
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
        self.logging.info(f"USAGE_STATS {self.usage_stats}")
        return self.usage_stats
        