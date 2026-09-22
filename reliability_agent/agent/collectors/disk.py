import shutil, psutil, logging, os
class DiskCollector:
    def __init__(self):
        self.usage_stats = []
        
    def collect(self):
        inode_perc = self.get_inode_perc()
        for partition in psutil.disk_partitions(all=True):
            if partition.mountpoint != '/': # the code trys to get the partition with the root
                continue
            try:
                usage = psutil.disk_usage('/')
                self.usage_stats.append({
                    "device": partition.device,
                    "mount_point": partition.mountpoint,
                    "usage_percent": usage.percent,
                    "inode_perc": inode_perc
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

    def get_inode_perc(self):
        stat = os.statvfs('/') # checking used inodes
        inode_used = stat.f_files-stat.f_ffree
        total_inode = stat.f_files
        return (inode_used/total_inode)*100
        