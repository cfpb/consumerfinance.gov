if [ -f /src/cfgov-refresh/.env ]; then
    source /src/cfgov-refresh/.env
    echo 'source /src/cfgov-refresh/.env' >> ~/.bashrc

fi
if [ -f /etc/profile.d/extend-environment ]; then
    source /etc/profile.d/extend-environment.sh
fi

ln -sf $PYTHON /usr/local/bin/python

exec "$@"
