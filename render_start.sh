#!/usr/bin/env bash
# render_start.sh

# Garante que os arquivos __init__.py existem
touch mytasks/__init__.py
touch tasks/__init__.py

# Executa migrações do banco de dados
python manage.py migrate --noinput

# Coleta arquivos estáticos
python manage.py collectstatic --noinput

# Inicia o servidor Gunicorn
gunicorn mytasks.wsgi:application
