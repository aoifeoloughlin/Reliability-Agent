import psutil
# psutil allows python to read and retrieve information on running processes

class CPUCollector:

    def __init__(self):
        self.prev_sample = None
        self.cur_sample = None

    def read_proc_stat(self):
        if(self.cur_sample == None):
            self.cur_sample = psutil.cpu_times()
        else:
            self.prev_sample = cur_sample
            self.cur_sample = psutil.cpu_times()
            
        
    def calculate_delta_percentage(self, stat_interval_prev, stat_interval_cur):
        total_active_prev = (stat_interval_prev.user +stat_interval_prev.nice + stat_interval_prev.system + stat_interval_prev.irq + stat_interval_prev.idle + stat_interval_prev.iowait+stat_interval_prev.softirq)
        total_idle_prev = (stat_interval_prev.idle+stat_interval_prev.iowait)

        total_active_cur = (stat_interval_cur.user +stat_interval_cur.nice + stat_interval_cur.system + stat_interval_cur.irq + stat_interval_cur.idle + stat_interval_cur.iowait+stat_interval_cur.softirq)
        total_idle_cur = (stat_interval_cur.idle+stat_interval_cur.iowait)

        delta_total_active = total_active_cur-total_active_prev
        delta_total_idle = total_idle_cur - total_idle_prev

        return self.calculate_cpu_percentage(delta_total_active, delta_total_idle)


    def calculate_cpu_percentage(self, total_active, total_idle):
        cpu_usage_perc=( 100 * (total_active - total_idle) / total_active )
        return cpu_usage_perc

    def collect(self):
        print("in collect")
        self.read_proc_stat()

        if(self.prev_sample == None):
            print("prev sample is none", self.prev_sample)
            return
        else:
            cpu_perc = self.calculate_delta_percentage(self.prev_sample, self.cur_sample)
            print("CPU PERC:", cpu_perc)
            return cpu_perc
