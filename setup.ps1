# Create directories
New-Item -ItemType Directory -Force -Path docker
New-Item -ItemType Directory -Force -Path app/bot
New-Item -ItemType Directory -Force -Path app/core
New-Item -ItemType Directory -Force -Path app/utils

# Create Docker files
New-Item -ItemType File -Force -Path docker/Dockerfile
New-Item -ItemType File -Force -Path docker/docker-compose.yml
New-Item -ItemType File -Force -Path .dockerignore

# Create Python files
New-Item -ItemType File -Force -Path app/__init__.py
New-Item -ItemType File -Force -Path app/main.py
New-Item -ItemType File -Force -Path app/bot/__init__.py
New-Item -ItemType File -Force -Path app/bot/handler.py
New-Item -ItemType File -Force -Path app/core/__init__.py
New-Item -ItemType File -Force -Path app/core/config.py
New-Item -ItemType File -Force -Path app/utils/__init__.py
New-Item -ItemType File -Force -Path app/utils/setup_webhook.py

# Create config files
New-Item -ItemType File -Force -Path requirements.txt
New-Item -ItemType File -Force -Path .env
New-Item -ItemType File -Force -Path .gitignore

Write-Host "Project structure created successfully!" 