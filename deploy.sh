#!/bin/bash
echo "🚀 Deploying Mentora..."
docker build -t mentora . && \
docker tag mentora us-central1-docker.pkg.dev/mentora-djapp/mentora/mentora:latest && \
docker push us-central1-docker.pkg.dev/mentora-djapp/mentora/mentora:latest && \
gcloud run services update mentora --region us-central1 --image us-central1-docker.pkg.dev/mentora-djapp/mentora/mentora:latest
echo "✅ Done!"