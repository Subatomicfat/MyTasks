#!/usr/bin/env bash
# render_start.sh

# Garante que os arquivos __init__.py existem
touch mytasks/__init__.py
touch tasks/__init__.py

# Executa migrações
python manage.py migrate --noinput

# Coleta arquivos estáticos (agora com STATIC_ROOT configurado)
python manage.py collectstatic --noinput

# Inicia o servidor
gunicorn mytasks.wsgi:application
