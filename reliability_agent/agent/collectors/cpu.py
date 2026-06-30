import psutil, time
# psutil allows python to read and retrieve information on running processes

class CPUCollector:

    def __init__(self):
        self.prev_sample = None
        self.cur_sample = None

    def read_proc_stat(self):
        self.prev_sample = 0
        self.cur_sample = 0
        self.prev_sample = psutil.cpu_times()
        time.sleep(1)
        self.cur_sample = psutil.cpu_times()
            
        print("CUR_SAMPLE", self.cur_sample)
            
        
    def calculate_delta_percentage(self, stat_interval_prev, stat_interval_cur):
        total_prev = (stat_interval_prev.user +stat_interval_prev.nice + stat_interval_prev.system + stat_interval_prev.irq + stat_interval_prev.idle + stat_interval_prev.iowait+stat_interval_prev.softirq+stat_interval_prev.steal)
        
        total_active_prev = (stat_interval_prev.user +stat_interval_prev.nice + stat_interval_prev.system + stat_interval_prev.irq +stat_interval_prev.softirq+stat_interval_prev.steal)
        
        total_idle_prev = (stat_interval_prev.idle+stat_interval_prev.iowait)

        total_cur = (stat_interval_cur.user +stat_interval_cur.nice + stat_interval_cur.system + stat_interval_cur.irq + stat_interval_cur.idle + stat_interval_cur.iowait+stat_interval_cur.softirq+stat_interval_cur.steal)
        
        total_active_cur = (stat_interval_cur.user +stat_interval_cur.nice + stat_interval_cur.system + stat_interval_cur.irq +stat_interval_cur.softirq+stat_interval_cur.steal)
        
        total_idle_cur = (stat_interval_cur.idle+stat_interval_cur.iowait)

        delta_total_active = total_active_cur - total_active_prev
        delta_total = total_cur-total_prev
        delta_total_idle = total_idle_cur - total_idle_prev

        return self.calculate_cpu_percentage(delta_total_active, delta_total_idle, delta_total)


    def calculate_cpu_percentage(self, total_active, total_idle, total):
        print("total_active ", total_active, " total_prev ", total_idle, " total ", total)
        cpu_usage_perc=( (100 * (total - total_idle)) / total )
        return cpu_usage_perc

    def collect(self):
        self.read_proc_stat()
        cpu_perc = self.calculate_delta_percentage(self.prev_sample, self.cur_sample)
        print("CPU PERC:", cpu_perc)

        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"CPU CHECK PERC: {cpu_percent}%")
        return cpu_perc
