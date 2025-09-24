#!/bin/bash
# Build and push Docker image to GitHub Container Registry

set -e

# Configuration
IMAGE_NAME="ghcr.io/hoangsonmoitapcode/fraud-detection-api"
TAG="latest"

echo "🔨 Building Docker image..."
docker build -t $IMAGE_NAME:$TAG .

echo "📦 Pushing to GitHub Container Registry..."
docker push $IMAGE_NAME:$TAG

echo "✅ Build and push completed!"
echo "🚀 Image available at: $IMAGE_NAME:$TAG"
echo ""
echo "To deploy on Railway:"
echo "1. Go to Railway dashboard"
echo "2. Create new service from Docker image"
echo "3. Use image: $IMAGE_NAME:$TAG"
