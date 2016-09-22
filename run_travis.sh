echo "running $RUNTEST"
if [ "$RUNTEST" == "frontend" ]; then
    gulp lint
    gulp "test:unit"
    gulp "test:coveralls"
elif [ "$RUNTEST" == "backend" ]; then
    tox -e travis
    coveralls
fi
