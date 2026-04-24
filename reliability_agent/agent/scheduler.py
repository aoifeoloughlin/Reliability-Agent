import time, logging, signal

class Scheduler:
    def __init__(self, interval):
        self.running = True
        self.interval = interval

    def stop(self):
        # This method is called from main.py for the graceful shut down
        self.running = False
        logging.info("Scheduler has been stopped...")
    
    def futureTask(self):
        print("Hello from future task")

    def run(self):
        print("Scheduler has started....")

        while self.running:
            self.futureTask()
            time.sleep(self.interval)
            signal.signal(signal.SIGTERM, stop) # SIGTERM is what systemd sends 
            signal.signal(signal.SIGINT, stop) # This is for hitting Ctrl+C
        
