#!/bin/bash
set -e
# Set mc alias for MinIO (idempotent)
mc alias set minio http://minio:9000 minioadmin minioadmin123 || true
# Start n8n (as node user)
su node -c "n8n"