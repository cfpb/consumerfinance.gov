# if docker ps succeeds, docker environment is already sane and
# we don't need to mess with docker-machine
docker ps 2>/dev/null
if [ $? -eq 0 ]; then
  echo "docker machine up and running!"
  DOCKER_SANE=1
else
   MACHINE_IP=$(docker-machine ip)
    if [ -z "$MACHINE_IP" ]; then
      echo "No default docker machine found, creating one now..."
      docker-machine create default --driver virtualbox\
        --virtualbox-cpu-count "2"\
        --virtualbox-memory "3072" 
    fi
    # harmless if the machine is already up:
    echo "Starting docker machine..."
    docker-machine start
    # inject environment variables needed for docker/compose:
    eval $(docker-machine env)
fi

echo "Setting MySQL and Elasticsearch envvars..."
MACHINE_IP=$(docker-machine ip)
export MYSQL_HOST="$MACHINE_IP"
export MYSQL_NAME='v1'
export MYSQL_USER='v1'
export MYSQL_PASSWORD='v1'
export ES_HOST="$MACHINE_IP"
