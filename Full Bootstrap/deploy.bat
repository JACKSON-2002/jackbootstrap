@echo off
echo.
echo ================================
echo Bootstrap Learning Website
echo GitHub Deployment Script
echo ================================
echo.

REM Check if username is provided
if "%1"=="" (
    echo ERROR: Please provide your GitHub username
    echo Usage: deploy.bat YOUR_GITHUB_USERNAME
    echo Example: deploy.bat johnsmith
    pause
    exit /b 1
)

set GITHUB_USERNAME=%1
set REPO_NAME=bootstrap-learning-website

echo Setting up GitHub repository for user: %GITHUB_USERNAME%
echo Repository name: %REPO_NAME%
echo.

REM Add remote origin
echo Adding GitHub remote...
git remote add origin https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git

REM Push to GitHub
echo Pushing to GitHub...
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================
    echo SUCCESS! Repository deployed!
    echo ================================
    echo.
    echo Your website will be available at:
    echo https://%GITHUB_USERNAME%.github.io/%REPO_NAME%
    echo.
    echo Next steps:
    echo 1. Go to your GitHub repository settings
    echo 2. Enable GitHub Pages with "GitHub Actions" source
    echo 3. Wait 2-3 minutes for deployment
    echo.
) else (
    echo.
    echo ================================
    echo DEPLOYMENT FAILED
    echo ================================
    echo.
    echo Please check:
    echo 1. Make sure you created the repository on GitHub first
    echo 2. Verify your GitHub username is correct
    echo 3. Ensure you have push permissions
    echo.
)

pause
