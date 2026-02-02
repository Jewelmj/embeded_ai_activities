#!/bin/bash
set -e
trap 'echo "❌ Setup failed at line $LINENO"; exit 1' ERR

echo "📦 Setting up Edge AI Pipeline environment..."

# Create directories
mkdir -p data/images pipeline utils

# Install dependencies
pip3 install -r requirements.txt --quiet

# Download sample data only if empty
if [ -z "$(ls -A data/images)" ]; then
    echo "📥 Downloading sample images..."
    wget -q -P data/images https://raw.githubusercontent.com/opencv/opencv/master/samples/data/lena.jpg
    wget -q -P data/images https://raw.githubusercontent.com/opencv/opencv/master/samples/data/baboon.jpg
fi

echo "✅ Setup complete."