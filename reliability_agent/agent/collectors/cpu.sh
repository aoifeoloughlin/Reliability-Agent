#!/usr/bin/env bash
#sudo +x agent/collectors/cpu.sh - need to make this a sub issue
local total_idle total_active cpu_usage
read -r cpu user nice system idle iowait irq softirq _ < <(grep '^cpu ' /proc/stat)
total_idle=$((idle + iowait))
total_active=$((user + nice + system + irq + softirq))
cpu_usage=$(( 100 * (total_active - total_idle) / total_active ))
echo "CPU Usage: $cpu_usage %"
json_string=$(jq -n \
    --argjson total_idle "$total_idle" \
    --argjson total_active "$total_active" \
    --argjson cpu_usage "$cpu_usage" \
    '{total_idle: $total_idle, total_active: $total_active, cpu_usage: $cpu_usage}')
echo "JSON CPU: $json_string"
