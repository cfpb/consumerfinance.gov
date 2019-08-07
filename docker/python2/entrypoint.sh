source /src/cfgov-refresh/.env
source /etc/profile.d/extend-environment.sh
export DB_HOST=$(python -c "from six.moves.urllib.parse import urlparse;import os; print(urlparse(os.environ['DATABASE_URL']).hostname)")
wait-for-it.sh $DB_HOST:5432 -t 0
python2.7 /src/cfgov-refresh/cfgov/manage.py runserver 0.0.0.0:8000
