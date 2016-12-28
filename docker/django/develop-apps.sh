#!/bin/sh

for d in /src/develop-apps/*/ ; do
        export PYTHONPATH=$d:$PYTHONPATH
done
