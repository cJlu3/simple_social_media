#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <service-path> <ssh-port> [remote-target=/srv/app]" >&2
  exit 1
fi

SERVICE_PATH=$(realpath "$1")
SSH_PORT="$2"
REMOTE_PATH="${3:-/srv/app}"

if [[ ! -d "$SERVICE_PATH" ]]; then
  echo "Service path '$SERVICE_PATH' does not exist" >&2
  exit 1
fi

ARCHIVE_NAME=$(basename "$SERVICE_PATH")

echo "[push-service] Packing '$SERVICE_PATH' and streaming to dev@localhost:$REMOTE_PATH (port $SSH_PORT)"

tar -C "$SERVICE_PATH" -czf - . | ssh -p "$SSH_PORT" -o StrictHostKeyChecking=no dev@localhost "mkdir -p '$REMOTE_PATH/$ARCHIVE_NAME' && tar -xzf - -C '$REMOTE_PATH/$ARCHIVE_NAME'"

echo "[push-service] Done. Files are now in $REMOTE_PATH/$ARCHIVE_NAME inside the remote container."

