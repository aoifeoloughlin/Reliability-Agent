import time, signal, logging, threading, os, subprocess, sys, pickle
from agent.json_formatter import JsonFormatter
from agent.logging_content import get_logger
from agent.metric_store import MetricsStore
from agent.log_event_enum import LogEvent as LogEvent
from pathlib import Path
from agent.scheduler import Scheduler
from agent.config_loader import ConfigLoader
from agent.collectors.cpu import CPUCollector
running = True

logger = get_logger()
cpu_collector = CPUCollector()

# Handle shut down gracefully
def handle_shutdown(sigum, frame):
    global running
    logger.info(str(LogEvent.HANDLE_SHUTDOWN_SIGNAL_RECEIVED), extra={"sigum":sigum, "running":running})
    running = False

def run_collectors():
    print("in the run collectors")
    cpu = cpu_collector.collect()
    #memory = memory_collector...etc

def main():
    global running
    # Load Config
    config_loader = ConfigLoader("../reliability_agent/configs/agent.yaml")
    agent_config = config_loader.load_config()
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