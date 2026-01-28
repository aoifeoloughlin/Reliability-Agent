# Detectors
- Decide if it's bad by judging the data.

## Files/Folders in the directory:
- init:
- cpu_pressure.py: Detects the sustained CPU saturation. Uses load average vs core count.
- memory_leak.py: Detects rising memory usage over time and avoids false positives with trend analysis.
- disk_full.py: Detects disk usage beyond the safe thresholds. Flags the failure.
- thresholds
- trends