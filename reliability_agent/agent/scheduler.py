import time, logging

class Scheduler:
    def __init__(self, interval):
        self.running = True
        self.interval = interval

    def stop(self):
        # This method is called from main.py for the graceful shut down
        self.running = False
        logging.INFO("Scheduler has been stopped...")
    
    def futureTask():
        logging.INFO("Hello from future task")

    def running(self):
        logging.INFO("Scheduler has started....")

        while self.running:
            futureTask()
            time.sleep(self.interval)
        
