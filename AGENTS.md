# Agents and Automation Overview

This file contains an overview of all agents and automated components within this repository, including tips for productivity and future development.

## Repository Structure

- **app.py** – Main Flask application with background task queue and dynamic blueprint registration.
- **app_utils.py** – Utility functions for payload validation, queue wrapping, and job logging.
- **config.py** – Loads environment variables and validates storage provider settings.
- **generate_docs.py** – CLI script that generates endpoint documentation using the Anthropic API.
- **generate_vector.sh** – Shell script that collates repository text into a single vector document.
- **local.sh** – Builds and runs the Docker container locally using variables from `.env_variables.json`.
- **docker-entrypoint-n8n.sh** – Entrypoint script for the custom n8n container.
- **Dockerfile / Dockerfile.n8n** – Container build instructions for the toolkit and for n8n.
- **docker-compose.yml** – Deploys the toolkit with Traefik.
- **docker-compose.local.minio.n8n.yml** – Local development stack with MinIO and n8n.
- **tests/** – Unit tests for utilities and configuration.

## Agents

### 1. NCA Toolkit API Application

- **Location:** `app.py`
- **Function:** Starts the Flask API, dynamically loads blueprints from the `routes` directory (if present) and processes incoming tasks. Tasks are queued or executed immediately based on the `queue_task` decorator. Results can be sent to a webhook URL.
- **Trigger:** Run via `python app.py` or through Docker/Gunicorn. Endpoints are exposed over HTTP.
- **Dependencies:** Flask, environment variables (`API_KEY`, storage settings), `app_utils`, `version.py` for build numbers.
- **Tips:**
  - Ensure required environment variables are set before starting the application.
  - Extend functionality by adding new blueprints in a `routes` folder. The `discover_and_register_blueprints` utility will automatically register them.
  - Webhook callbacks depend on an external module `services.webhook`. Provide an implementation when deploying.

### 2. Documentation Generator

- **Location:** `generate_docs.py`
- **Function:** Reads Python endpoint files, calls the Anthropic API (Claude) with a custom prompt, and writes Markdown documentation to an output directory.
- **Trigger:** Command line: `python generate_docs.py <source_path> [--force]`.
- **Dependencies:** `requests`, `.env_shell.json` containing `ANTHROPIC_API_KEY` and `API_DOC_OUTPUT_DIR`.
- **Tips:**
  - Use the `--force` flag to regenerate docs even if files were recently updated.
  - Consider adding timeouts to HTTP requests as recommended in `AUDIT_REPORT.md`.
  - Suitable for automation in a CI workflow to keep API docs up to date.

### 3. Local Development Runner

- **Location:** `local.sh`
- **Function:** Stops any running toolkit containers, builds the Docker image, reads variables from `.env_variables.json`, and runs the container for testing.
- **Trigger:** Manual execution: `bash local.sh`.
- **Dependencies:** Docker, `jq`, `.env_variables.json` with environment variables.
- **Tips:**
  - Useful for quickly iterating on local changes.
  - Verify that Docker is installed and `.env_variables.json` is properly filled.

### 4. Vector Document Generator

- **Location:** `generate_vector.sh`
- **Function:** Scans the repository for markdown, text, Python files, and Dockerfiles, excluding specific patterns. Appends the content of each file to `NCA Toolkit API Vector Doc.txt`.
- **Trigger:** Manual execution: `bash generate_vector.sh`.
- **Dependencies:** Bash utilities (`find`, `sed`, etc.).
- **Tips:**
  - The generated file can be used for building embeddings or search indexes.
  - Review excluded filenames to ensure important files are not omitted.

### 5. n8n Entrypoint Script

- **Location:** `docker-entrypoint-n8n.sh`
- **Function:** Configures the MinIO CLI (`mc`) and starts n8n under the `node` user inside the custom n8n container.
- **Trigger:** Automatically executed when the n8n Docker container starts.
- **Dependencies:** n8n base image, MinIO CLI.
- **Tips:**
  - Customize the entrypoint if additional bootstrapping is required.

### 6. Docker Compose Services

- **Locations:** `docker-compose.yml`, `docker-compose.local.minio.n8n.yml`
- **Function:** Define multi-container setups. The main compose file deploys Traefik and the toolkit. The local development variant adds MinIO and n8n for workflow automation and storage.
- **Trigger:** `docker compose up -d` with the chosen file.
- **Dependencies:** Docker, environment variables (`.env`, `.env.local.minio.n8n`).
- **Tips:**
  - Use the local MinIO/n8n stack for testing complex workflows.
  - Adjust port mappings if conflicts occur.

## Productivity Suggestions

- **Automate Documentation Generation:** Integrate `generate_docs.py` into a CI workflow to automatically refresh endpoint documentation when routes change.
- **Expand Test Coverage:** Current tests cover utilities and configuration. Add tests for `app.py` and any future route modules to ensure stable behaviour.
- **Combine Local Scripts:** `local.sh` and `generate_vector.sh` could be merged into a unified development script or Makefile for easier onboarding.
- **Improve Error Handling:** Follow the recommendations from `AUDIT_REPORT.md` (e.g., bind to localhost by default, configurable temp paths, HTTP timeouts).
- **Document Missing Modules:** Provide an implementation or stub for `services.webhook` and any dynamic routes to help new contributors get started quickly.

