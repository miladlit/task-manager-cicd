
#!/bin/bash
set -e

echo "Checking Task Manager deployment..."

# Wait until the application responds
for i in {1..10}; do
    if curl -fsS http://localhost:8000/health > /dev/null; then
        echo "Health check passed!"

        # Check which Docker image is running
        image=$(docker inspect --format '{{.Config.Image}}' task-manager-demo)

        if [ "$image" = "task-manager:v2" ]; then
            echo "Correct version deployed: $image"
            echo "Deployment verified successfully!"
            exit 0
        fi

        echo "Wrong version: $image"
        exit 1
    fi

    echo "Waiting for application..."
    sleep 2
done

echo "Deployment verification failed!"
docker logs task-manager-demo
exit 1
