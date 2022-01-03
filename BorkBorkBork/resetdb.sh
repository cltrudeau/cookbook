#!/bin/bash

find . -name "*.pyc" -exec rm {} \;
rm db.sqlite3

# django db and test data process
python manage.py wipe_migrations
python manage.py makemigrations core 
python manage.py migrate

echo "=== Creating Data ==="
python manage.py create_test_admin
python manage.py recipes ../data/recipes/
