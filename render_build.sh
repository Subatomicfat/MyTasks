#!/usr/bin/env bash
# render_build.sh

# Instala todas as dependências do requirements.txt
pip install -r requirements.txt

# Instala explicitamente o dj-database-url como fallback
pip install dj-database-url==1.3.0

# Coleta arquivos estáticos
python manage.py collectstatic --noinput
