import time, logging, signal, threading
from agent.logging_content import get_logger
from agent.metric_store import MetricsStore
from agent.log_event_enum import LogEvent as LogEvent
from agent.collectors.cpu import CPUCollector
from agent.collectors.memory import MemoryCollector
from agent.collectors.disk import DiskCollector

class Scheduler:
    def __init__(self, running, interval, window_size):
        self.running = running
        self.interval = interval
        self.disk = None
        self.tick_count = 0
        self.logger = get_logger()
        self.metric_store = MetricsStore(window_size)
        self.cpu_collector = CPUCollector()
        self.memory_collector = MemoryCollector()
        self.disk_collector = DiskCollector()

    def run_collectors(self):
        cpu = self.cpu_collector.collect()
        memory = self.memory_collector.collect()
        self.disk = self.disk_collector.collect()
        logger.info(LogEvent.COLLECTED_METRICS, extra={"cpu_perc":cpu, "memory_used_perc":memory, "disk_usage_stats":self.disk})

    def run(self, run_thread, stop_thread, detectors_functions):
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
                    detectors_functions()
                    duration = time.monotonic()-start
                    self.metric_store.add_sample(LogEvent.TICK_COMPLETED.value, self.tick_count)
                    self.metric_store.add_sample(LogEvent.TICK_DURATION.value, duration)
                    self.logger.info(f"Tick {self.tick_count} completed in {duration:.2f}s", extra={"duration":duration, "tick_count":self.tick_count})
            except Exception as e:
                self.logger.error(f"Worker crashed with error: {e}")
        self.metric_store.print_metrics()