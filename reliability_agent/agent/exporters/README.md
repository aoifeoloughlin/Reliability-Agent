# Exporters

- Exposes signals. How we see what's happening.

## Files in the directory:
- init:
- prometheus.py: Exposes the metrics in a Prometheus format.
- json_logs.py: Structured logs and makes them machine-readable. Enables correlation during incidents.
- healthz.py: Has HTTP endpoint and reports agent health and system status.