import time, signal, logging, threading, os, subprocess, sys, pickle
from agent.json_formatter import JsonFormatter
from agent.logging_content import get_logger
from agent.metric_store import MetricsStore
from agent.log_event_enum import LogEvent as LogEvent
from pathlib import Path
from agent.scheduler import Scheduler
from agent.config_loader import ConfigLoader
from agent.collectors.cpu import CPUCollector
from agent.collectors.memory import MemoryCollector
from agent.collectors.disk import DiskCollector
from agent.detectors.disk_detection import DiskDetector
running = True

def __init__(self, threshold=80):
    self.disk = None
    self.disk_config = None

logger = get_logger()
cpu_collector = CPUCollector()
memory_collector = MemoryCollector()
disk_collector = DiskCollector()
disk_detector = DiskDetector()

# Handle shut down gracefully
def handle_shutdown(sigum, frame):
    global running
    logger.info(str(LogEvent.HANDLE_SHUTDOWN_SIGNAL_RECEIVED), extra={"sigum":sigum, "running":running})
    running = False

def run_collectors():
    cpu = cpu_collector.collect()
    memory = memory_collector.collect()
    self.disk = disk_collector.collect()
    logger.info(LogEvent.COLLECTED_METRICS, extra={"cpu_perc":cpu, "memory_used_perc":memory, "disk_usage_stats":self.disk})

def run_detectors():
    disk_detection =  disk_detector.detect(self.disk_config, self.disk)
    logger.info(LogEvent.COLLECTED_METRICS, extra={"disk thresh":disk_detection})


def main():
    global running
    # Load Config
    agent_config_loader = ConfigLoader("../reliability_agent/configs/agent.yaml")
    agent_config = agent_config_loader.load_config()
    disk_config_loader = ConfigLoader("../reliability_agent/detectors/thresholds/disk_thresholds.yaml")
    self.disk_config = disk_config_loader.load_config()
    interval = agent_config["interval_seconds"]
    window_size = agent_config["window_size"]
    scheduler = Scheduler(running, interval, window_size)
    next_run = time.monotonic()
    metric_store = MetricsStore(window_size)
    logger.info(LogEvent.RELIABILITY_AGENT_STARTED.value, extra={"interval_seconds":interval, "next_run":next_run})

    # Ensure that if you or Systemd end the loop is can handle the shutdown
    signal.signal(signal.SIGTERM, handle_shutdown) # SIGTERM is what systemd sends 
    signal.signal(signal.SIGINT, handle_shutdown) # This is for hitting Ctrl+C

    run_thread = threading.Event()
    stop_thread = threading.Event()
    thread = threading.Thread(target=scheduler.run, args=(run_thread, stop_thread, run_collectors), daemon=True)
    thread.start()
    logger.info(str(LogEvent.THREAD_STARTED), extra={"running":running})

    # Start Loop
    while running:
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
    main()