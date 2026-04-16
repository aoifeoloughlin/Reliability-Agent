import time, signal, logging, sleep

running = True

# Handle shut down gracefully
def handle_shutdown(sigum, frame):
    global running
    logging.info(f"Received signal {signum}, shutting down...")
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
    logging.basicConfig(level=logging.INFO) # Actual config parsing will be added in future issues
    interval = 5
    logging.info("Start Reliability Agent")

    # Ensure that if you or Systemd end the loop is can handle the shutdown
    signal.signal(signal.SIGTERM, handle_shutdown) # SIGTERM is what systemd sends 
    signal.signal(signal.SIGINT, handle_shutdown) # This is for hitting Ctrl+C

    # Start Loop
    while running:
        collect_metrics() # collects the system metrics
        detect_issues() # finds the issues in the metrics
        sleep(interval) # prevents loop oversaturation 

# When running the python command by calling the main directly this is what makes it run
# This is the entry point
if __name__ == "__main__":
    main()