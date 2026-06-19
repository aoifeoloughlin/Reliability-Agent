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
stats_json=$(jq -n \
    --argjson user "$user" \
    --argjson nice "$nice" \
    --argjson system "$system" \
    --argjson idle "$idle" \
    --argjson iowait "$iowait" \
    --argjson irq "$irq" \
    --argjson softirq "$softirq" \
    --argjson steal "$steal" \
    '{user:${user:-0},nice:${nice:-0},system:${system:-0},idle:${idle:-0},iowait:${iowait:-0},irq:${irq:-0},softirq:${softirq:-0}}' \
    2>&1)

echo "$stats_json"

echo "user=$user"
echo "nice=$nice"
echo "system=$system"
echo "idle=$idle"
echo "iowait=$iowait"
echo "irq=$irq"
echo "softirq=$softirq"
