#!/bin/bash

# Check if docker is installed.
if [ -x "$(command -v docker)" ]; then
  echo "Docker is installed."
else
  echo "Docker not installed. See installation.md for installing docker."
fi

# If docker ps succeeds, docker environment is already sane and
# we don't need to mess with docker-machine.
if [ ! -z "$(docker ps)" ]; then
  echo "You've already got a working docker setup!"
else
  echo "Maybe we just need to start your default docker machine..."
  if [ -z "$(docker-machine ip)" ]; then
    echo "No default docker machine found, creating one with virtualbox..."
    docker-machine create default --driver virtualbox\
      --virtualbox-cpu-count "2"\
      --virtualbox-memory "3072"
    vboxmanage controlvm default natpf1 "http,tcp,,8000,,8000"
    vboxmanage controlvm default natpf1 "https,tcp,,8443,,8443"
    vboxmanage controlvm default natpf1 "browsersync,tcp,,3000,,3000"
    vboxmanage controlvm default natpf1 "browsersyncui,tcp,,3001,,3001"
  fi
  # Harmless if the machine is already up:
  echo "Starting your machine..."
  if [ ! -z "$(docker-machine start)" ];then
    echo "...started!"
  fi
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
