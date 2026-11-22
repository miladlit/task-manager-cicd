#!/bin/bash
set -e
# Legacy rollback demo preserved (requires the old v2 image).
echo "Starting Task Manager deployment (legacy v2 demo)..."
docker image inspect task-manager:v2 > /dev/null
docker rm -f task-manager-demo 2>/dev/null || true
docker run -d --name task-manager-demo -p 8000:8000 task-manager:v2
echo "Version 2 deployment started!"
