#!/bin/sh
set -eu
# Read-only checks; can be run over SSH on your Coolify host.
printf '\n=== HOST ===\n'
uname -a
printf '\n=== MEMORY ===\n'
free -h
printf '\n=== DISK ===\n'
df -h / /var/lib/docker 2>/dev/null || df -h /
printf '\n=== DOCKER SPACE ===\n'
docker system df
printf '\n=== DOCKER LIVE USAGE (trim output before sharing) ===\n'
docker stats --no-stream --format 'table {{.Name}}\t{{.MemUsage}}\t{{.CPUPerc}}'
