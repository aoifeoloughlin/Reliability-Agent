# Reliability-Agent
A Python daemon running on Linux. Monitors system health. Detects faulty conditions and oversatuaration. It triggers automated remediation and then restart services. Emits structured logs and metrics, and exposes a /healthz endpoint.

## Problem Statement

Linux systems commonly experience failures due to gradual resource exhaustion, such as sustained CPU pressure, memory leaks, or disk saturation. These issues often develop over time and are not effectively captured by simple threshold-based monitoring, which can miss early warning signs or generate noisy alerts.

As a result, engineers are frequently forced into reactive incident response, addressing problems only after system performance has already degraded or outages have occurred.

There is a need for a lightweight, host-level solution that can detect early indicators of system instability, provide actionable signals, and safely perform limited remediation to reduce operational burden and improve system reliability.

### Background
Ideally the system runs unaffected by resource exhaustion or external faults. However, this is an unrealistic case, therefore downtime is to be expected. Although excessive downtime comes with creating issues for users and stress for Engineers. Making it undesirable and frustrating to use said service.

### Relevance
Having a light-weight Reliability Agent will prevent long periods of downtime, as well as, automating the service restart, helping to reduce the loss of revenue and resources. 

### Objectives
The primary ojective is prevent massive periods of downtime. Saving time and resources. 
#### Specific Objectives
- Create a Python daemon that runs a reliability agent 
- Make the agent collect and analyze metrics of the system's tools
- Analyze metrics and detect potential CPU pressure, memory leaks, and disk saturation
- If required restart services that may have reached limits or have shutdown
- Use a metrics exporter to display the data logged

## Non-Goals
- Replacing full observability platforms (e.g., Prometheus, Datadog)
  This agent provides local insights and signals, not a complete monitoring solution.

- Distributed or multi-node coordination
  The agent is designed to run on a single Linux host and does not handle cluster-wide state or orchestration.

- Kubernetes or container orchestration support
  This project focuses on host-level reliability rather than container scheduling or orchestration systems.

- Aggressive or irreversible remediation actions
  The agent avoids destructive actions (e.g., killing arbitrary processes, deleting data) and prioritizes safe, reversible operations.

- Real-time guarantees or hard latency constraints
  The agent operates on periodic polling and does not aim to provide real-time monitoring.

- Deep application-level diagnostics
  The focus is on system-level signals (CPU, memory, disk), not application-specific logic or tracing.

## Files/Folders in this directory:
- pyproject.toml: Projects the metadata. Has the tools config and python version. Basically a package.
- requirements.txt: Has runtime dependencies only. Creates an easy installation on Linux hosts.

## Running the Agent's main:
`python -m agent.main` or `python3 -m agent.main`  