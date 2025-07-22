# GitHub Repository Setup - PowerShell Script
# Run this script after creating a GitHub repository manually

# Repository details
$REPO_NAME = "bootstrap-learning-website"
$GITHUB_USERNAME = "YOUR_GITHUB_USERNAME"  # Replace with your actual GitHub username

Write-Host "Setting up GitHub repository..." -ForegroundColor Green

# Set the default branch to main
git branch -M main

# Add GitHub remote origin
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

# Push to GitHub
git push -u origin main

Write-Host "Repository successfully pushed to GitHub!" -ForegroundColor Green
Write-Host "Your website will be available at: https://$GITHUB_USERNAME.github.io/$REPO_NAME" -ForegroundColor Cyan
