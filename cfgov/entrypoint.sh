for d in /src/cfgov-refresh/develop-apps/*/ ; do
    export PYTHONPATH=$d:$PYTHONPATH
done
python /src/cfgov-refresh/cfgov/manage.py runserver 0.0.0.0:8000
