#!/usr/bin/env bash
# render_build.sh

# Instala dependências
pip install -r requirements.txt

# Coleta arquivos estáticos
python manage.py collectstatic --noinput

# Executa migrações do banco de dados
python manage.py migrate
