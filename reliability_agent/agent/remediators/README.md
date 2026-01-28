# Remediators

- Fixes it.
- Ever action is idempotent, rate-limited, reversible.

## Files in the directory

- init:
- restart_service.py: Restaarts the `systemd` services and verifies the recovery.
- rotate_logs.py: Forces log rotation and prevents disk exhaustion.
- scale_workers.py: Dynamically adjusts worker process counts and reduces overload.