
# Task Manager   CI/CD Project



This is my final project for the CI/CD course at Nackademin.

I created a simple Task Manager API using Python and FastAPI. The main purpose of this project is to learn how CI/CD works and how to automate testing and deployment.

The application is simple because my main focus is on the CI/CD process.

## What the Application Does

The application allows users to:

- Create a task
- View all tasks
- Delete a task
- Check if the application is running
- Check the application version

The API can be tested in the browser at:

http://localhost:8000/docs

## Tools I Used

- **Python and FastAPI:** To build the application.
- **Git and GitHub:** To save and manage the code.
- **GitHub Actions:** To automate the CI/CD pipeline.
- **Pytest:** To test the application.
- **Ruff:** To check code quality.
- **Docker:** To run the application in a container.
- **Bash:** To automate deployment and rollback.

## How My CI/CD Pipeline Works

When I push code to GitHub, GitHub Actions starts automatically.

The pipeline:

1. Downloads the code.
2. Runs automated tests using Pytest.
3. Checks the code using Ruff.
4. Saves the test results.
5. Builds a Docker image.
6. Starts the application in a Docker container.
7. Checks if the application works.
8. Stops and removes the container.

If a test or code check fails, the Docker build does not continue.

This helps prevent broken code from moving further in the process.

## How to Run the Project

First, install the Python packages:

```bash
python -m pip install -r requirements.txt
```

Start the application:

```bash
python -m uvicorn app.main:app --reload
```

Open this address in your browser:

http://localhost:8000/docs

## Testing

Run the automated tests:

```bash
python -m pytest -v
```

Check the code with Ruff:

```bash
python -m ruff check app tests
```

## Docker

Build the Docker image:

```bash
docker build -t task-manager:local .
```

Run the container:

```bash
docker run --rm -p 8000:8000 task-manager:local
```

Check if the application works:

http://localhost:8000/health

## Deployment and Rollback

I created three Bash scripts to make deployment easier.

- `deploy_local.sh` starts version 2 of the application.
- `verify.sh` checks that the application is running and the correct image is used.
- `rollback_local.sh` restores the previous version.

The scripts are inside the `scripts` folder.

They can be run using:

```bash
bash scripts/deploy_local.sh
bash scripts/verify.sh
bash scripts/rollback_local.sh
```

The deployment and rollback scripts use Docker images `task-manager:v1` and `task-manager:v2`, which need to be built locally first.

## Testing a Failed Pipeline

I also tested what happens when something goes wrong.

I changed one test on purpose so it would fail.

GitHub Actions detected the problem and stopped the Docker build.

After fixing the test and pushing the changes again, the pipeline passed.

This showed me why automated testing is important.


## Conclusion

This project helped me understand how CI/CD works in practice.

The most important thing I learned is that CI/CD is not just about automating commands. It is about finding problems early, testing changes and making software delivery safer.

There are still things I could improve, such as adding a database, more tests and deployment to a real server.
