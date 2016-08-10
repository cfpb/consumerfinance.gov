cp -R -n /apps/ .
python cfgov/manage.py migrate
python cfgov/manage.py runscript initial_data
python cfgov/manage.py runserver 0.0.0.0:8000


