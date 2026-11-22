#!/bin/bash
set -e
# Legacy version verification for v2 demo container.
echo "Checking Task Manager legacy deployment..."
for i in {1..10}; do
  if curl -fsS http://localhost:8000/health > /dev/null; then
    image=$(docker inspect --format '{{.Config.Image}}' task-manager-demo)
    if [ "$image" = "task-manager:v2" ]; then
      echo "Health and version verified: $image"
      exit 0
    fi
    echo "Wrong version: $image"
    exit 1
  fi
  sleep 2
done
echo "Deployment verification failed!"
docker logs task-manager-demo
exit 1
