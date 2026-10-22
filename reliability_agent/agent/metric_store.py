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
            print(self.to_dict())
            file.write(json.dumps(self.to_dict(), indent=2))

    def to_dict(self):
        return asdict(self.metrics) #{t: [asdict(self.metrics) for metric_sample in self.metrics] for t, self.metrics in self._buf.items()}