# Deployment Directory

This directory contains all deployment-related files and configurations.

## Structure

```
deployment/
├── railway/              # Railway deployment files
│   ├── setup-railway.ps1
│   ├── setup-railway-env.ps1
│   ├── test-railway-api.ps1
│   ├── railway.json
│   ├── Procfile
│   ├── runtime.txt
│   └── RAILWAY_DEPLOYMENT_GUIDE.md
├── docker/               # Docker deployment files
│   └── Dockerfile
└── scripts/              # Deployment scripts
```

## Railway Deployment

### Quick Start
1. Run `deployment/railway/setup-railway.ps1`
2. Run `deployment/railway/setup-railway-env.ps1`
3. Test with `deployment/railway/test-railway-api.ps1`

### Files
- **setup-railway.ps1**: Main Railway setup script
- **setup-railway-env.ps1**: Environment variables setup
- **test-railway-api.ps1**: API testing script
- **railway.json**: Railway configuration
- **Procfile**: Process definition for Railway
- **runtime.txt**: Python runtime version
- **RAILWAY_DEPLOYMENT_GUIDE.md**: Detailed deployment guide

## Docker Deployment

- **Dockerfile**: Container configuration
- **.dockerignore**: Files to ignore in Docker build
