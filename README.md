# Reliability-Agent
A Python daemon running on Linux. Monitors system health. Detects faulty conditions and oversatuaration. It triggers automated remediation and then restart services. Emits structured logs and metrics, and exposes a /healthz endpoint.

## Files/Folders in this directory:
- pyproject.toml: Projects the metadata. Has the tools config and python version. Basically a package.
- requirements.txt: Has runtime dependencies only. Creates an easy installation on Linux hosts.