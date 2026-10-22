from collections import defaultdict, deque
from dataclasses import asdict
import json

class MetricsStore:
    def __init__(self, window_size):
        self.window_size = window_size
        self.metrics = defaultdict(
            lambda: deque(maxlen=self.window_size)
        )
        self._buf = {t: deque(maxlen=window_size) for t in self.metrics}

    def add_sample(self, metric_name, value):
        self.metrics[metric_name].append(value)
        print(self.metrics[metric_name])
    
    def print_metrics(self):
        with open('metrics_logs.json', 'w') as file:
            file.write(json.dumps(self.getLastNSamples(self.window_size), indent=2, default=str))

    def getLastNSamples(self, window_size):
        while(len(self.metrics) > window_size and len(self.metrics > 1)):
            self.metrics.popleft()
        return list(self.metrics)