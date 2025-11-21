#!/bin/bash

# Mind Healer Backend - Docker Image Build Script

IMAGE_NAME="mindhealer-backend"
IMAGE_TAG="latest"

echo "=========================================="
echo "Building Docker Image: ${IMAGE_NAME}:${IMAGE_TAG}"
echo "=========================================="

# Build Docker image
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Build Success!"
    echo "=========================================="
    echo "Image: ${IMAGE_NAME}:${IMAGE_TAG}"
    echo ""
    echo "Available commands:"
    echo "  docker images | grep ${IMAGE_NAME}"
    echo "  docker run -d -p 8000:8000 --name mindhealer ${IMAGE_NAME}:${IMAGE_TAG}"
    echo "=========================================="
else
    echo ""
    echo "=========================================="
    echo "❌ Build Failed!"
    echo "=========================================="
    exit 1
fi
