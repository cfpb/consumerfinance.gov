source /src/cfgov-refresh/.env
source /etc/profile.d/extend-environment.sh
python /src/cfgov-refresh/cfgov/manage.py runserver 0.0.0.0:8000
