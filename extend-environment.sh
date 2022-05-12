# shopt -s nullglob

for d in /src/consumerfinance.gov/develop-apps/*/ ; do
    export PYTHONPATH=$d:$PYTHONPATH
done
