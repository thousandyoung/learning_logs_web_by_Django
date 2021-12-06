import os
os.system('virtualenv venv; source venv/bin/activate;  '
          'pip install -r requirements.txt; '
          'pip install django-taggit; '
          'python manage.py makemigrations;'
          'python manage.py migrate; '
          'python manage.py makemigrations learning_logs;'
          'python manage.py makemigrate;'
          'python manage.py runserver;'
          )