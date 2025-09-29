#!/usr/bin/env python3
import os
import uvicorn

# Set HF_TOKEN environment variable
os.environ['HF_TOKEN'] = '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'
os.environ['PYTHONPATH'] = os.getcwd()

print("🔑 HF_TOKEN set:", bool(os.getenv('HF_TOKEN')))
print("📁 PYTHONPATH set:", os.getenv('PYTHONPATH'))
print("🚀 Starting server with model loading capabilities...")

# Start server
uvicorn.run('src.main:app', host='0.0.0.0', port=8000, reload=False)
