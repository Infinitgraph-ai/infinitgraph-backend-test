# Docker Setup for Infinitgraph Document Analyzer

## Prerequisites
- Docker installed on your system
- Docker Compose installed on your system

## Environment Setup

1. Create a `.env` file in the project root with the following variables:
   ```
   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_BASE_URL=https://api.openai.com/v1
   LLM_MODEL=gpt-3.5-turbo
   
   # JWT Authentication
   JWT_SECRET_KEY=your_jwt_secret_key_here
   JWT_ALGORITHM=HS256
   ```

## Building and Running with Docker

### Using Docker Compose (Recommended)

1. Build and start the container:
   ```bash
   docker compose up -d
   ```

2. Access the API:
   - API documentation: http://localhost:8000/docs
   - API endpoint: http://localhost:8000/api/

3. Stop the container:
   ```bash
   docker compose down
   ```

### Using Docker directly

1. Build the Docker image:
   ```bash
   docker build -t infinitgraph-analyzer .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 --env-file .env infinitgraph-analyzer
   ```

## Development with Docker

The docker-compose configuration includes a volume mount that syncs your local code with the container, allowing you to make changes without rebuilding:

```yaml
volumes:
  - .:/app
```

After making code changes, restart the container to apply them:
```bash
docker compose restart
```

## VS Code Development Container

This project includes a devcontainer configuration for Visual Studio Code, which allows you to work inside a Docker container directly from VS Code.

### Prerequisites

- VS Code installed
- [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension installed

### Getting Started with Devcontainer

1. Open the project folder in VS Code
2. When prompted, click "Reopen in Container" or use the command palette (F1) and select "Remote-Containers: Reopen in Container"
3. VS Code will build the container and set up the development environment with:
   - Python extension
   - Pylance for improved intellisense
   - Code formatting tools (Black, Autopep8)
   - Linting tools (Pylint, MyPy)
   - Docker extension

### Benefits

- Consistent development environment across team members
- All dependencies pre-installed
- Debugging and development tools configured automatically
- Seamless integration with Docker-based deployment 