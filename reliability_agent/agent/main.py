import time, signal, logging, threading
from agent.scheduler import Scheduler
from agent.config_loader import ConfigLoader
running = True

# Handle shut down gracefully
def handle_shutdown(sigum, interval):
    global running
    logging.info(f"Received signal {sigum}, shutting down...")
    running = False

# Collects metrics
def collect_metrics():
    logging.info(f"Collecting metrcis...(stub)")

# Detect issues
def detect_issues():
    logging.info(f"Detecting issues...(stub)")

def main():
    global running

    # Load Config
    agentConfig = ConfigLoader(None)
    logging.info(agentConfig)
    interval = 5

    logging.info("Start Reliability Agent")

    # Ensure that if you or Systemd end the loop is can handle the shutdown
    signal.signal(signal.SIGTERM, handle_shutdown) # SIGTERM is what systemd sends 
    signal.signal(signal.SIGINT, handle_shutdown) # This is for hitting Ctrl+C

    scheduler = Scheduler(running, interval)

    thread = threading.Thread(target=scheduler.run)
    thread.start()

    # Start Loop
    while running:
        print("collect and detect")
        collect_metrics() # collects the system metrics
        detect_issues() # finds the issues in the metrics
        print("sleep")
        time.sleep(interval) # prevents loop oversaturation 
    
    thread.join()
        

# When running the python command by calling the main directly this is what makes it run
# This is the entry point
if __name__ == "__main__":
    main()