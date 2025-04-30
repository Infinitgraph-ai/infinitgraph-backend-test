# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONPATH=/app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.8.0

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock /app/

RUN poetry lock

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
CMD ["task", "run"]