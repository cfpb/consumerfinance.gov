source /etc/profile.d/extend-environment.sh
ln -sf /usr/bin/python3.6 /usr/local/bin/python
python3.6 /src/cfgov-refresh/cfgov/manage.py runserver 0.0.0.0:8000
