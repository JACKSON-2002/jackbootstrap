#!/bin/bash

# GitHub Repository Setup Script
# Run this script after creating a GitHub repository manually

# Repository details
REPO_NAME="bootstrap-learning-website"
GITHUB_USERNAME="YOUR_GITHUB_USERNAME"  # Replace with your actual GitHub username

# Set the default branch to main
git branch -M main

# Add GitHub remote origin
git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git

# Push to GitHub
git push -u origin main

echo "Repository successfully pushed to GitHub!"
echo "Your website will be available at: https://$GITHUB_USERNAME.github.io/$REPO_NAME"
