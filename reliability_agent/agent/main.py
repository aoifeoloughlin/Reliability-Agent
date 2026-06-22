import time, signal, logging, threading, os, subprocess, sys
import agent.json_formatter import JsonFormatter
from pathlib import Path
from agent.scheduler import Scheduler
from agent.config_loader import ConfigLoader
running = True

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
logger = logging.getLogger("agent")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Handle shut down gracefully
def handle_shutdown(sigum, frame):
    global running
    logging.info(f"Received signal {sigum}, shutting down...", extra={"sigum":sigum, "running":running})
    running = False

# Collects metrics
def collect_metrics():
    current_dir = Path(__file__).resolve().parent
    script_path = current_dir / 'collectors' / 'cpu.sh'
    result = subprocess.run([script_path], capture_output=True, text=True)
    logging.info(f"Collecting metrcis...(stub)", extra={"result":result.stdout.strip(),"path":script_path})


# Detect issues
def detect_issues():
    logging.info(f"Detecting issues...(stub)")

def main():
    global running
    # Load Config
    config_loader = ConfigLoader("../reliability_agent/configs/agent.yaml")
    agent_config = config_loader.load_config()
    interval = agent_config["interval_seconds"]
    scheduler = Scheduler(running, interval)
    next_run = time.monotonic()
    logging.info("Start Reliability Agent", extra={"interval_seconds":interval, "next_run":next_run})

    # Ensure that if you or Systemd end the loop is can handle the shutdown
    signal.signal(signal.SIGTERM, handle_shutdown) # SIGTERM is what systemd sends 
    signal.signal(signal.SIGINT, handle_shutdown) # This is for hitting Ctrl+C

    run_thread = threading.Event()
    stop_thread = threading.Event()
    thread = threading.Thread(target=scheduler.run, args=(run_thread, stop_thread), daemon=True)
    thread.start()
    logging.info("Thread started", extra={"thread":thread, "running":running})

    # Start Loop
    while running:
        if time.monotonic() >= next_run:
            run_thread.set()
            collect_metrics() # collects the system metrics
            detect_issues() # finds the issues in the metrics
            next_run += interval
    stop_thread.set() #stops the while loop in the scheduler class
    thread.join() #cleans up multi-threading
    logging.info("Thread ended", extra={"time_monotonic":time.monotonic, "next_run":next_run})
        
# When running the python command by calling the main directly this is what makes it run
# This is the entry point
if __name__ == "__main__":
    main()