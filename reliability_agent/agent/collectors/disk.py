import shutil, psutil
class DiskCollector:
    def __init__(self):
        self.PSEUDO_FILESYSTEMS = {
            'proc', 
            'sysfs', 
            'devfs', 
            'devtmpfs', 
            'tmpfs',
            'cgroup', 
            'cgroup2',
            'pstore', 
            'debugfs', 
            'mqueue', 
            'hugetlbfs', 
            'securityfs',
            'iso9660', 
            'udf',
            '/snap/'
        }
        self.usage_stats = []
        
    def collect(self):
        for partition in psutil.disk_partitions(all=False):
            print(f"Total partitions found: {len(psutil.disk_partitions(all=False))}")
            if partition.fstype in self.PSEUDO_FILESYSTEMS:
                continue
            if partition.device.startswith('/dev/loop'):  
                continue
            try:
                usage = psutil.disk_usage(partition.mountpoint)
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
        