import time, psutil

class MemoryCollector:
    def __init__(self):
        self.prev_sample = None
        self.cur_sample = None

    def read_proc_meminfo(self):
        self.prev_sample = psutil.virtual_memory()
        time.sleep(1)
        self.cur_sample = psutil.virtual_memory()

    def calculate_used_memory_perc(self):
        delta_total = self.cur_sample.total - self.prev_sample.total
        delta_available = self.cur_sample.available - self.prev_sample.available
        delta_percent = ((delta_total - delta_available)/delta_total)*100
        return delta_percent


    def collect(self):
        self.read_proc_meminfo()
        memory_used_perc = self.calculate_used_memory_perc()
        return memory_used_perc