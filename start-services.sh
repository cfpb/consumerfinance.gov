#/bin/bash
echo "Setting up docker environment..."
source ./docker-environment.sh
echo "Docker environment setup complete!"

echo "Starting docker services"
docker-compose up -d
echo "MySQL and Elasticsearch are now setup in docker!"
