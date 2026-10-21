import time, logging, signal, threading
from agent.logging_content import get_logger
from agent.metric_store import MetricsStore
from agent.log_event_enum import LogEvent as LogEvent
from agent.collectors.cpu import CPUCollector
from agent.collectors.memory import MemoryCollector
from agent.collectors.disk import DiskCollector
from agent.config_loader import ConfigLoader
from agent.detectors.disk_detection import DiskDetector

class Scheduler:
    def __init__(self, running, interval, window_size):
        self.running = running
        self.interval = interval
        self.disk = None
        self.cpu = None
        self.memory = None
        self.tick_count = 0
        self.timestamp = None
        self.wallclock = None
        self.logger = get_logger()
        self.metric_store = MetricsStore(window_size)
        self.cpu_collector = CPUCollector()
        self.memory_collector = MemoryCollector()
        self.disk_collector = DiskCollector()
        disk_config_loader = ConfigLoader("../reliability_agent/agent/detectors/thresholds/disk_thresholds.yaml")
        self.disk_config = disk_config_loader.load_config()
        self.disk_detector = DiskDetector()

    def run_collectors(self):
        self.cpu = self.cpu_collector.collect()
        self.memory = self.memory_collector.collect()
        self.disk = self.disk_collector.collect()
        self.add_to_metrics_store(self.cpu, self.memory, self.disk)
        self.logger.info(LogEvent.COLLECTED_METRICS, extra={"cpu_perc":self.cpu, "memory_used_perc":self.memory, "disk_usage_stats":self.disk})

    def run_detectors(self):
        disk_detection =  self.disk_detector.detect(self.disk_config, self.disk)
        self.logger.info(LogEvent.DETECTION_STARTED, extra={"disk thresh":disk_detection})

    def add_to_metrics_store(self, cpu, mem, disk):
        self.timestamp = time.monotonic()
        self.wallclock = datetime.now(timezone.utc)
        cpu_val = { "ts": self.timestamp, "wall": self.wallclock, "value": cpu}
        mem_val = { "ts": self.timestamp, "wall": self.wallclock, "value": mem}
        disk_val = { "ts": self.timestamp, "wall": self.wallclock, "value": disk}
        self.metric_store.add_sample(LogEvent.CPU.value, cpu_val)
        self.metric_store.add_sample(LogEvent.MEMORY.value, mem_val)
        self.metric_store.add_sample(LogEvent.DISK_USAGE.value, disk_val)
        print("METRIC STORE VALUE PRINTED", LogEvent.TICK_COMPLETED.value, " ",LogEvent.TICK_DURATION.value)

    def run(self, run_thread, stop_thread):
        while not stop_thread.is_set():
            try:
                thread = run_thread.wait(timeout=0.5)
                if stop_thread.is_set():
                    break
                if thread:
                    run_thread.clear()
                    self.logger.info(LogEvent.SCHEDULER_SIGNAL_RECEIVED)
                    self.tick_count += 1
                    start=time.monotonic()
                    self.run_collectors()  
                    self.run_detectors()
                    duration = time.monotonic()-start
                    self.logger.info(f"Tick {self.tick_count} completed in {duration:.2f}s", extra={"duration":duration, "tick_count":self.tick_count})
            except Exception as e:
                self.logger.error(f"Worker crashed with error: {e}")
        self.metric_store.print_metrics()