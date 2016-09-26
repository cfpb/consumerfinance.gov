echo "running $RUNTEST tests"
if [ "$RUNTEST" == "frontend" ]; then
    gulp "test:unit"
    gulp "test:coveralls"
elif [ "$RUNTEST" == "backend" ]; then
    tox -e travis
    coveralls
fi
