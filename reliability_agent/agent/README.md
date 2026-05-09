# Agent
- Mirrors real production agents like "Datadog Agent" and/or "Node Exporter".
- Has all runtime logic

## Files/Folders in this directory:
- main.py: Entry point of the agent. It starts the schduler. It wires together collectors -> detectors -> remediators -> exporters. Where `systemd` starts execution.
- config.py: Loads the YAML config files. Provides the default settings and valids the configuration. Let's you tune the variables.
- scheduler.py: Runs periodic tasks at set intervals. Makes the execution predictable. Ensures graceful shutdown. 
- state.py: Stores the in-memory history, like previous metrics, trend data and cooldowns.

## Notes about Scheduler
It runs tasks periodically using asynchronous multi-threading. Called from the main class.