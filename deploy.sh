#!/bin/bash
# Quick deployment script

echo "🚀 Fraud Detection API - Deployment Script"
echo "=========================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📝 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - Fraud Detection API v3.1.1"
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Committing latest changes..."
    git add .
    git commit -m "Update: $(date '+%Y-%m-%d %H:%M:%S')"
fi

echo ""
echo "🎯 Deployment Options:"
echo "1. Railway (Recommended - Free tier)"
echo "2. Render (Free tier with sleep mode)"
echo "3. Heroku (Paid)"
echo "4. Manual GitHub setup"

read -p "Choose option (1-4): " choice

case $choice in
    1)
        echo "🚂 Deploying to Railway..."
        if ! command -v railway &> /dev/null; then
            echo "Installing Railway CLI..."
            npm install -g @railway/cli
        fi
        
        echo "Please run: railway login"
        echo "Then run: railway new"
        echo "Finally run: railway up"
        ;;
    2)
        echo "🎨 Setting up for Render..."
        echo "1. Push code to GitHub"
        echo "2. Go to render.com"
        echo "3. Connect your GitHub repo"
        echo "4. Set environment variables"
        echo "5. Deploy!"
        ;;
    3)
        echo "🟣 Setting up for Heroku..."
        if ! command -v heroku &> /dev/null; then
            echo "Please install Heroku CLI first"
            exit 1
        fi
        
        read -p "Enter your app name: " app_name
        heroku create $app_name
        heroku addons:create heroku-postgresql:mini -a $app_name
        git push heroku main
        ;;
    4)
        echo "📚 Manual GitHub Setup:"
        echo "1. Create GitHub repository"
        echo "2. git remote add origin <your-repo-url>"
        echo "3. git push -u origin main"
        echo "4. Connect to your preferred platform"
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "✅ Deployment setup complete!"
echo ""
echo "📋 Post-deployment checklist:"
echo "- [ ] Test API health: curl <your-url>/health"
echo "- [ ] Test phone analysis: curl <your-url>/analyze/"
echo "- [ ] Check interactive docs: <your-url>/docs"
echo "- [ ] Monitor logs for errors"
echo "- [ ] Set up custom domain (optional)"
echo ""
echo "🎉 Your API will be available at: https://your-app-name.platform.app"
