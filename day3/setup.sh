#!/bin/bash
set -e
trap 'echo "❌ Setup failed at line $LINENO"; exit 1' ERR

echo "📦 Setting up Embedded Edge AI environment..."

# Install Python dependencies into active environment
python3 -m pip install -r requirements.txt --quiet

echo "✅ Setup complete."
echo "You can now run: python main.py"