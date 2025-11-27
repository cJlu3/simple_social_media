#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 3 ]]; then
  echo "Usage: $0 <sql-file> <ssh-port> <psql-connection-string>" >&2
  echo "Example: $0 ./seed.sql 2223 \"postgresql://postgres:postgres@localhost:5432/postgres\"" >&2
  exit 1
fi

SQL_FILE=$(realpath "$1")
SSH_PORT="$2"
CONN_STR="$3"

if [[ ! -f "$SQL_FILE" ]]; then
  echo "SQL file '$SQL_FILE' does not exist" >&2
  exit 1
fi

echo "[push-sql] Copying $(basename "$SQL_FILE") to remote host (port $SSH_PORT)"
scp -P "$SSH_PORT" -o StrictHostKeyChecking=no "$SQL_FILE" dev@localhost:/tmp/seed.sql

echo "[push-sql] Applying script via psql"
ssh -p "$SSH_PORT" -o StrictHostKeyChecking=no dev@localhost "psql \"$CONN_STR\" -f /tmp/seed.sql"

echo "[push-sql] Done"

