#!/usr/bin/env bash
#sudo +x agent/collectors/cpu.sh - need to make this a sub issue
local total_idle total_active cpu_usage
read -r cpu user nice system idle iowait irq softirq _ < <(grep '^cpu ' /proc/stat)
total_idle = $((idle + iowait))
total_active = $((user + nice + system + idle + irq + softirq))
echo "total $total_active"
cpu_usage=$((100 * ((total_active-total_idle)/total_active)))
echo "CPU_Usage: $cpu_usage %"