#!/usr/bin/env bash
read -r _ user nice system idle iowait irq softirq steal _ < /proc/stat
total_idle = $((idle + iowait))
total_active = $((user+nice+system+idle+iowait+irq+softirq+steal))

cpu_usage=$((100 * ((total_active-total_idle)/total_active)))
echo "CPU_Usage: $cpu_usage%"