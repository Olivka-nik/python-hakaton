#!/bin/zsh
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"
PYTHON_BIN="python3"

cd "$PROJECT_DIR"

if [[ ! -f "manage.py" ]]; then
  echo "Ошибка: manage.py не найден в $PROJECT_DIR"
  exit 1
fi

if ! "$PYTHON_BIN" -c "import django" >/dev/null 2>&1; then
  echo "Django не найден. Устанавливаю..."
  "$PYTHON_BIN" -m pip install django
fi

echo "Применяю миграции..."
"$PYTHON_BIN" manage.py migrate

echo "Запускаю сервер: http://127.0.0.1:8000/ (без autoreload)"
"$PYTHON_BIN" manage.py runserver 127.0.0.1:8000 --noreload
