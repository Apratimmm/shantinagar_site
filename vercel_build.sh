#!/bin/bash
set -e

echo "Installing dependencies..."
npm install
pip install -r requirements.txt

echo "Building CSS..."
npm run build:css

echo "Running database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build complete!"
