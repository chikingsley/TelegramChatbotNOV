#!/bin/bash

# Create directories
mkdir -p docker app/bot app/core app/utils

# Create Docker files
touch docker/Dockerfile
touch docker/docker-compose.yml
touch .dockerignore

# Create Python files
touch app/__init__.py
touch app/main.py
touch app/bot/__init__.py
touch app/bot/handler.py
touch app/core/__init__.py
touch app/core/config.py
touch app/utils/__init__.py
touch app/utils/setup_webhook.py

# Create config files
touch requirements.txt
touch .env
touch .gitignore

# Set execute permissions
chmod +x setup.sh

echo "Project structure created successfully!" 