import time, signal, threading
from agent.json_formatter import JsonFormatter
from agent.logging_content import get_logger
from agent.metric_store import MetricsStore
from agent.log_event_enum import LogEvent as LogEvent
from agent.scheduler import Scheduler
from agent.config_loader import ConfigLoader
running = True

logger = get_logger()

class ReliabilityAgent:
    def __init__(self):
        self.running = True
        agent_config_loader = ConfigLoader("../reliability_agent/configs/agent.yaml")
        self.agent_config = agent_config_loader.load_config()

       
    # Handle shut down gracefully
    def handle_shutdown(self, sigum, frame):
        logger.info(str(LogEvent.HANDLE_SHUTDOWN_SIGNAL_RECEIVED), extra={"sigum":sigum, "running":running})
        self.running = False

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
        thread = threading.Thread(target=scheduler.run, args=(run_thread, stop_thread), daemon=True)
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