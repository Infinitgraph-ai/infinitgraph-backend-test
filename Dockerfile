# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock /app/

# Install dependencies using Poetry
RUN poetry install --no-root

# Copy the application code into the container
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Install Taskfile binary
RUN apt-get update && apt-get install -y curl && \
    curl -sL https://taskfile.dev/install.sh | sh && \
    mv ./bin/task /usr/local/bin/task && \
    rm -rf ./bin && apt-get clean && rm -rf /var/lib/apt/lists/*

# Command to run the application using Taskfile
CMD ["/bin/bash", "-c", "task run"]