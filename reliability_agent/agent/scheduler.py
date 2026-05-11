import time, logging, signal, threading

class Scheduler:
    def __init__(self, running, interval):
        self.running = running
        self.interval = interval
    
    def futureTask(self):
        print("Hello from future task")

    def run(self, run_thread, stop_thread):
        while not stop_thread.is_set():
            try:
                thread = run_thread.wait(timeout=0.5)
                if stop_thread.is_set():
                    break
                if thread:
                    run_thread.clear()
                    print("Scheduler: Signal received, starting work!")
                    self.futureTask()  
            except Exception as e:
                print(f"Worker crashed with error: {e}")