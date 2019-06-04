if [ -f /src/cfgov-refresh/.env ]; then
    source /src/cfgov-refresh/.env
    echo 'source /src/cfgov-refresh/.env' >> ~/.bashrc

fi
if [ -f /etc/profile.d/extend-environment ]; then
    source /etc/profile.d/extend-environment.sh
fi

export PATH=/active-python:$PATH
ln -sf $PYTHON /active-python/python

exec "$@"
