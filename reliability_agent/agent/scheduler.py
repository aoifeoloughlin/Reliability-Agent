import time, logging, signal, threading

class Scheduler:
    def __init__(self, running, interval):
        self.running = running
        self.interval = interval
        self.tick_count = 0
    
    def futureTask(self):
        logging.info("Hello from future task")

    def run(self, run_thread, stop_thread):
        while not stop_thread.is_set():
            self.tick_count += 1
            try:
                thread = run_thread.wait(timeout=0.5)
                if stop_thread.is_set():
                    break
                if thread:
                    run_thread.clear()
                    logging.info("Scheduler: Signal received, starting work!")
                    start=time.monotonic()
                    self.futureTask()  
                    duration = time.monotonic()-start
                    logging.info(f"Tick {self.tick_count} completed in {duration:.2f}s", extra={"duration"=duration, "tick_count"=self.tick_count})
            except Exception as e:
                logging.error(f"Worker crashed with error: {e}")