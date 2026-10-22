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
        # data = {
        #     metric_type: [asdict(metric_sample) for metric_sample in self.metrics]     
        #     for metric_type, self.metrics in self._buf.items()
        # }
        with open('metrics_logs.json', 'w') as file:
            file.write(json.dumps(self.to_dict(), indent=2))

    def to_dict(self):
        return {t: [asdict(metric_sample) for metric_sample in self.metrics] for t, self.metrics in self._buf.items()}