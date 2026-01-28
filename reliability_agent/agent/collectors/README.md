# Collectors

- This reads the system's state.
- Only reads from `/proc`, `/sys` and system cmds.

## Files in the directory:
- init
- cpu.py: Reads CPU stats from `/proc/stat` and calculates usage percentages.
- memory.py: Reads from `/proc/meminfo` and calculates the available memory vs the used memory.
- disk.py: Uses `df` or `/proc/mounts` and detects disk and inode exhaustion.
- network.py: Reads from `/proc/net/dev` and tracks the RX/TX throughput and errors.