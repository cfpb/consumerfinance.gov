#!/bin/bash

# if docker ps succeeds, docker environment is already sane and
# we don't need to mess with docker-machine
docker ps 2>/dev/null
if [ $? -eq 0 ]; then
  echo "You've already got a working docker setup!"
else
   echo "Maybe we just need to start your default docker machine..."
   MACHINE_IP=$(docker-machine ip)
    if [ -z "$MACHINE_IP" ]; then
      echo "No default docker machine found, creating one with virtualbox..."
      docker-machine create default --driver virtualbox\
        --virtualbox-cpu-count "2"\
        --virtualbox-memory "3072" 
    fi
    # harmless if the machine is already up:
    echo "Starting your machine..."
    docker-machine start
    echo "You've got a working docker machine, yay!"
    eval $(docker-machine env)
fi

cat <<END

Here are some useful commands:

  Set up your current terminal: eval \$(docker-machine env)
    (if you ran this file with 'source', then that is already done for you)
  run the site: docker-compose up
  open up a shell into the python container: ./shell.sh
  stop and start the VM: docker-machine stop (or start)

Further reading:
  https://docs.docker.com/machine/
  https://docs.docker.com/compose/
END
