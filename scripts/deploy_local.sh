
#!/bin/bash
set -e

echo "Starting Task Manager deployment..."

# Check that version 2 exists
docker image inspect task-manager:v2 > /dev/null

# Remove the previous demo container
docker rm -f task-manager-demo 2>/dev/null || true

# Deploy version 2
docker run -d \
  --name task-manager-demo \
  -p 8000:8000 \
  task-manager:v2

echo "Version 2 deployment started!"
