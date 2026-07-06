import shutil
class DiskCollector:

    def read_disk_usage(path):
        total, used, free = shutil.disk_usage(path)
        print((used/total) * 100)
        return (used/total) * 100


