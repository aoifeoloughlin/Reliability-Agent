import time, logging, signal, threading

class Scheduler:
    def __init__(self, running, interval, thread):
        self.running = running
        self.interval = interval
        self.thread = thread

    def stop(self):
        # This method is called from main.py for the graceful shut down
        self.running = False
        logging.info("Scheduler has been stopped...")
    
    def futureTask(self):
        print("Hello from future task")

    def run(self):
        while self.running:
            self.thread.wait()
            print("Scheduler: Signal received, starting work!")
            self.futureTask()
            self.thread.clear()
            
        
