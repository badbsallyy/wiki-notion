#!/bin/bash

# Setup script for wiki-notion project
# This script clones the deepsite repository from Hugging Face

echo "Setting up wiki-notion project..."
echo "Cloning deepsite repository from Hugging Face..."

git clone https://huggingface.co/spaces/enzostvs/deepsite

if [ $? -eq 0 ]; then
    echo "Successfully cloned deepsite repository!"
else
    echo "Failed to clone deepsite repository. Please check your internet connection and try again."
    exit 1
fi
