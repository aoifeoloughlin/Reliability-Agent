import time, logging, signal, threading
from agent.logging_content import get_logger
from agent.metric_store import MetricsStore()
from agent.log_event_enum import LogEvent as LogEvent

class Scheduler:
    def __init__(self, running, interval):
        self.running = running
        self.interval = interval
        self.tick_count = 0
        self.logger = get_logger()
        self.metric_store = MetricsStore()
        self.logEvent = LogEvent
    
    def futureTask(self):
        self.logger.info("Hello from future task")

    def run(self, run_thread, stop_thread):
        while not stop_thread.is_set():
            self.tick_count += 1
            try:
                thread = run_thread.wait(timeout=0.5)
                if stop_thread.is_set():
                    break
                if thread:
                    run_thread.clear()
                    self.logger.info(LogEvent.SCHEDULER_SIGNAL_RECEIVED)
                    start=time.monotonic()
                    self.futureTask()  
                    duration = time.monotonic()-start
                    metric_store.add_sample(self.logEvent.TICK_COMPLETED, tick_count)
                    metric_store.add_sample(self.logEvent.TICK_DURATION, duration)
                    self.logger.info(f"Tick {self.tick_count} completed in {duration:.2f}s", extra={"duration":duration, "tick_count":self.tick_count})
            except Exception as e:
                self.logger.error(f"Worker crashed with error: {e}")