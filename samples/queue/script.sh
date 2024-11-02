#!/bin/bash

# Define log directory and ensure it exists
LOG_DIR="system_logs"
mkdir -p "$LOG_DIR"

# Function to log command output
run_and_log() {
    local command=$1
    local log_file=$2
    echo "Running: $command"
    echo "Logging output to: $log_file"
    eval "$command" &> "$log_file"
}

# 1. System Information
run_and_log "uname -a" "$LOG_DIR/system_info.log"
run_and_log "df -h" "$LOG_DIR/disk_usage.log"
run_and_log "free -m" "$LOG_DIR/memory_usage.log"

# 2. List all users on the system
run_and_log "cat /etc/passwd" "$LOG_DIR/users.log"

# 3. Running processes
run_and_log "ps aux" "$LOG_DIR/running_processes.log"

# 4. Network configuration and connections
run_and_log "ifconfig" "$LOG_DIR/network_config.log"
run_and_log "netstat -tuln" "$LOG_DIR/listening_ports.log"
run_and_log "ss -tulnp" "$LOG_DIR/active_connections.log"

# 5. Disk usage by directory
run_and_log "du -sh /*" "$LOG_DIR/disk_usage_by_directory.log"

# 6. Last login attempts
run_and_log "last -a" "$LOG_DIR/last_logins.log"

echo "All commands have been executed and logged in the $LOG_DIR directory."
