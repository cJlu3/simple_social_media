#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  cat <<'USAGE' >&2
Usage:
  deploy-service.sh <service-path> <ssh-port> [remote-root=/srv/services] [app-port=8000] [env-file]

Example:
  scripts/deploy-service.sh ./auth_service 2226 /srv/services 8000 ./auth_service/.env
USAGE
  exit 1
fi

SERVICE_PATH=$(realpath "$1")
SSH_PORT="$2"
REMOTE_ROOT="${3:-/srv/services}"
APP_PORT="${4:-8000}"
ENV_FILE="${5:-}"

if [[ ! -d "$SERVICE_PATH" ]]; then
  echo "Service path '$SERVICE_PATH' not found" >&2
  exit 1
fi

SERVICE_NAME=$(basename "$SERVICE_PATH")
REMOTE_SERVICE_PATH="$REMOTE_ROOT/$SERVICE_NAME"

echo "[deploy:$SERVICE_NAME] Подготовка удалённого хоста (порт $SSH_PORT)..."
ssh -p "$SSH_PORT" -o StrictHostKeyChecking=no dev@localhost \
"set -euo pipefail
sudo apt-get update -y
sudo apt-get install -y python3-venv pipx tmux
pipx ensurepath >/dev/null 2>&1 || true
pipx install uv >/dev/null 2>&1 || true
mkdir -p '$REMOTE_SERVICE_PATH'
"

echo "[deploy:$SERVICE_NAME] Синхронизация исходников..."
rsync -az --delete "$SERVICE_PATH"/ dev@localhost:"$REMOTE_SERVICE_PATH"/

if [[ -n "$ENV_FILE" ]]; then
  if [[ ! -f "$ENV_FILE" ]]; then
    echo "ENV file '$ENV_FILE' not found" >&2
    exit 1
  fi
  echo "[deploy:$SERVICE_NAME] Копирование env..."
  scp -P "$SSH_PORT" -o StrictHostKeyChecking=no "$ENV_FILE" dev@localhost:"$REMOTE_SERVICE_PATH/.env"
fi

START_CMD="cd '$REMOTE_SERVICE_PATH' && \
if [[ ! -d .venv ]]; then python3 -m venv .venv; fi && \
source .venv/bin/activate && \
pip install --upgrade pip && \
pip install uv && \
uv pip install --editable . && \
tmux kill-session -t '$SERVICE_NAME' >/dev/null 2>&1 || true && \
tmux new -ds '$SERVICE_NAME' \"source .venv/bin/activate && uv run uvicorn src.main:app --host 0.0.0.0 --port $APP_PORT\""

echo "[deploy:$SERVICE_NAME] Установка зависимостей и запуск сервиса..."
ssh -p "$SSH_PORT" -o StrictHostKeyChecking=no dev@localhost "$START_CMD"

echo "[deploy:$SERVICE_NAME] Готово. Проверить логи: ssh dev@localhost -p $SSH_PORT 'tmux attach -t $SERVICE_NAME'"

