import time, signal, threading
from agent.json_formatter import JsonFormatter
from agent.logging_content import get_logger
from agent.metric_store import MetricsStore
from agent.log_event_enum import LogEvent as LogEvent
from agent.scheduler import Scheduler
from agent.config_loader import ConfigLoader
from agent.collectors.cpu import CPUCollector
from agent.collectors.memory import MemoryCollector
from agent.collectors.disk import DiskCollector
from agent.detectors.disk_detection import DiskDetector
running = True

logger = get_logger()

class ReliabilityAgent:
    def __init__(self):
        self.running = True
        self.disk = None

        agent_config_loader = ConfigLoader("../reliability_agent/configs/agent.yaml")
        self.agent_config = agent_config_loader.load_config()
        disk_config_loader = ConfigLoader("../reliability_agent/agent/detectors/thresholds/disk_thresholds.yaml")
        self.disk_config = disk_config_loader.load_config()
        
        self.cpu_collector = CPUCollector()
        self.memory_collector = MemoryCollector()
        self.disk_collector = DiskCollector()
        self.disk_detector = DiskDetector()

       
    # Handle shut down gracefully
    def handle_shutdown(self, sigum, frame):
        logger.info(str(LogEvent.HANDLE_SHUTDOWN_SIGNAL_RECEIVED), extra={"sigum":sigum, "running":running})
        self.running = False

    def run_collectors(self):
        cpu = self.cpu_collector.collect()
        memory = self.memory_collector.collect()
        self.disk = self.disk_collector.collect()
        logger.info(LogEvent.COLLECTED_METRICS, extra={"cpu_perc":cpu, "memory_used_perc":memory, "disk_usage_stats":self.disk})

    def run_detectors(self):
        disk_detection =  self.disk_detector.detect(self.disk_config, self.disk)
        logger.info(LogEvent.DETECTION_STARTED, extra={"disk thresh":disk_detection})


    def main(self):
        # Load Config
        
        interval = self.agent_config["interval_seconds"]
        window_size = self.agent_config["window_size"]
        scheduler = Scheduler(self.running, interval, window_size)
        next_run = time.monotonic()
        metric_store = MetricsStore(window_size)
        logger.info(LogEvent.RELIABILITY_AGENT_STARTED.value, extra={"interval_seconds":interval, "next_run":next_run})

        # Ensure that if you or Systemd end the loop is can handle the shutdown
        signal.signal(signal.SIGTERM, self.handle_shutdown) # SIGTERM is what systemd sends 
        signal.signal(signal.SIGINT, self.handle_shutdown) # This is for hitting Ctrl+C

        run_thread = threading.Event()
        stop_thread = threading.Event()
        thread = threading.Thread(target=scheduler.run, args=(run_thread, stop_thread, self.run_collectors, self.run_detectors), daemon=True)
        thread.start()
        logger.info(str(LogEvent.THREAD_STARTED), extra={"running":self.running})

        # Start Loop
        while self.running:
            if time.monotonic() >= next_run:
                run_thread.set()
                interval = float(interval)
                next_run += interval

        stop_thread.set() #stops the while loop in the scheduler class
        thread.join() #cleans up multi-threading
        logger.info(str(LogEvent.THREAD_ENDED), extra={"time_monotonic":time.monotonic(), "next_run":next_run})
        
            
    # When running the python command by calling the main directly this is what makes it run
    # This is the entry point
if __name__ == "__main__":
    agent = ReliabilityAgent()
    agent.main()