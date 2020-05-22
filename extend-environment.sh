shopt -s nullglob

for d in /src/cfgov-refresh/develop-apps/*/ ; do
    export PYTHONPATH=$d:$PYTHONPATH
done
