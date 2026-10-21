from collections import defaultdict, deque
import json

class MetricsStore:
    def __init__(self, window_size):
        self.window_size = window_size
        self.metrics = defaultdict(
            lambda: deque(maxlen=self.window_size)
        )

    def add_sample(self, metric_name, value):
        self.metrics[metric_name].append(value)
        print(self.metrics[metric_name])
    
    def print_metrics(self):
        for key, values in self.metrics.items():
            print(f"{key}: {list(values)}")
        
        with open('metrics_logs.json', 'w') as file:
            file.write(json.dumps(self.metrics, indent=4))
        