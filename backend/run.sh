#!/bin/bash

# Stop and remove old container
docker stop mindhealer-backend 2>/dev/null || true
docker rm mindhealer-backend 2>/dev/null || true

# Build image
docker build -t mindhealer-backend:latest .

# Load environment variables from .env
export $(cat .env | grep -v '^#' | xargs)

# Run container
docker run -d --name mindhealer-backend \
    -p 8000:8000 \
    --restart always \
    --hostname mindhealer-api \
    -e GOOGLE_API_KEY="${GOOGLE_API_KEY}" \
    -e GROQ_API_KEY="${GROQ_API_KEY:-}" \
    -e OPENAI_API_KEY="${OPENAI_API_KEY:-}" \
    -e TZ=Asia/Taipei \
    -v ${PWD}/books:/app/books \
    mindhealer-backend:latest

# Show logs
docker logs -f mindhealer-backend
