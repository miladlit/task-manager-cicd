#!/bin/bash
set -e
# Legacy rollback demo preserved (requires the old v1 image).
echo "Starting rollback to version 1..."
docker image inspect task-manager:v1 > /dev/null
docker rm -f task-manager-demo 2>/dev/null || true
docker run -d --name task-manager-demo -p 8000:8000 task-manager:v1
for i in {1..10}; do
  if curl -fsS http://localhost:8000/health; then
    echo
    echo "Rollback successful!"
    docker inspect --format '{{.Config.Image}}' task-manager-demo
    exit 0
  fi
  sleep 2
done
echo "Rollback verification failed!"
docker logs task-manager-demo
exit 1
