#!/usr/bin/env bash
# build.sh — Render runs this on every deploy
# Place this file next to manage.py
 
set -o errexit   # Exit immediately if any command fails
 
echo '═══════════════════════════════════════'
echo '  My_Portfolio — Render Build Script   '
echo '═══════════════════════════════════════'
 
# 1. Install Python dependencies
echo '▸ Installing requirements...'
pip install -r requirements.txt
 
# 2. Collect all static files into staticfiles/
echo '▸ Collecting static files...'
python manage.py collectstatic --no-input
 
# 3. Apply any pending database migrations
echo '▸ Running database migrations...'
python manage.py migrate
 
echo '✅ Build complete! Starting server...'
