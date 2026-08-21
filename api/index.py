"""Vercel serverless function entry point for the Django WSGI application."""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_ko_site.settings")

from school_ko_site.wsgi import application  # noqa: E402

app = application
