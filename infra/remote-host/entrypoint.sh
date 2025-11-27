#!/usr/bin/env bash
set -euo pipefail

mkdir -p /var/run/sshd

echo "[remote-host] $(date --iso-8601=seconds) container booted. SSH is on port 22."

exec /usr/sbin/sshd -D -e

