import time, psutil

class MemoryCollector:
    def __init__(self):
        self.prev_sample = None
        self.cur_sample = None

    def read_proc_meminfo(self):
        self.cur_sample = psutil.virtual_memory()

    def calculate_used_memory_perc(self):
        try:
            percent = ((self.cur_sample.total - self.cur_sample.available)/self.cur_sample.total)*100
            return percent
        except ZeroDivisionError:
            return 0.0


    def collect(self):
        self.read_proc_meminfo()
        memory_used_perc = self.calculate_used_memory_perc()
        return memory_used_perc